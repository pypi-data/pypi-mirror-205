use std::{
    collections::{HashMap, VecDeque},
    sync::Arc,
    time::{Duration, SystemTime, UNIX_EPOCH},
};

use neon::prelude::*;
use pyo3::prelude::*;
use serde::Serialize;
use tokio::{
    self,
    runtime::{Builder, Runtime},
    sync::{
        mpsc::{self, Sender},
        Mutex,
    },
    time::{sleep_until, Instant},
};

// TODO: Error handling

/// A Python module implemented in Rust.
#[derive(Serialize, Clone)]
#[serde(rename_all = "snake_case", tag = "plot_type")]
pub enum PlotType {
    Line { value: f64 },
    Counter { change: f64 },
    ProgressBar { value: f64, total: f64 },
}

#[derive(Serialize, Clone)]
struct Datapoint {
    #[serde(flatten)]
    plot_type: PlotType,
    plot_name: String,
    timestamp: u128,
}

struct FishingRod {
    riverbed_url: String,
    runtime: Runtime,
    http_client: reqwest::Client,
    api_key: String,
    datapoints_buffer: Arc<Mutex<Vec<Datapoint>>>,
}

fn get_nanoseconds_since_epoch() -> u128 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_nanos()
}

impl Finalize for FishingRod {}

impl FishingRod {
    pub fn new(riverbed_url: String, api_key: String) -> Self {
        let runtime = Builder::new_multi_thread()
            .worker_threads(1)
            .enable_all()
            .build()
            .unwrap();

        let datapoints_buffer = Arc::new(Mutex::new(Vec::new()));

        let rod = FishingRod {
            riverbed_url,
            runtime,
            api_key,
            http_client: reqwest::Client::new(),
            datapoints_buffer: datapoints_buffer,
        };

        rod.start_upload_loop();

        rod
    }

    fn start_upload_loop(&self) {
        let datapoints_buffer = self.datapoints_buffer.clone();
        let http_client = self.http_client.clone();
        let api_key = self.api_key.clone();
        let riverbed_url = self.riverbed_url.clone();
        self.runtime.spawn(async move {
            loop {
                {
                    let mut datapoints_buffer = datapoints_buffer.lock().await;

                    if !datapoints_buffer.is_empty() {
                        http_client
                            .post(format!("{}/datapoints", riverbed_url))
                            .bearer_auth(api_key.clone())
                            .json(&serde_json::to_value(datapoints_buffer.to_vec()).unwrap())
                            .send()
                            .await
                            .unwrap();
                    }

                    datapoints_buffer.clear()
                }
                sleep_until(Instant::now() + Duration::from_millis(100)).await;
            }
        });
    }

    async fn record_datapoint(&self, plot_name: String, plot_type: PlotType) {
        let mut datapoints_buffer = self.datapoints_buffer.lock().await;
        datapoints_buffer.push(Datapoint {
            plot_type,
            plot_name,
            timestamp: get_nanoseconds_since_epoch(),
        });
    }

    pub fn record_datapoint_blocking(&self, plot_name: String, plot_type: PlotType) {
        self.runtime
            .block_on(self.record_datapoint(plot_name, plot_type));
    }

    async fn clear(&self, plot_name: &str) {
        self.http_client
            .delete(format!("{}/plots/{}", self.riverbed_url, plot_name))
            .bearer_auth(self.api_key.clone())
            .send()
            .await
            .unwrap();
    }

    pub fn clear_blocking(&self, plot_name: &str) {
        self.runtime.block_on(self.clear(plot_name));
    }
}

// Python bindings

#[pyclass(name = "FishingRod")]
pub struct PythonFishingRod {
    rod: FishingRod,
}

#[pymethods]
impl PythonFishingRod {
    #[new]
    pub fn new(riverbed_url: String, api_key: String) -> Self {
        PythonFishingRod {
            rod: FishingRod::new(riverbed_url, api_key),
        }
    }

    pub fn line(&self, plot_name: String, value: f64) {
        self.rod
            .record_datapoint_blocking(plot_name, PlotType::Line { value });
    }

    pub fn counter(&self, plot_name: String, change: f64) {
        self.rod
            .record_datapoint_blocking(plot_name, PlotType::Counter { change });
    }

    pub fn progress_bar(&self, plot_name: String, value: f64, total: f64) {
        self.rod
            .record_datapoint_blocking(plot_name, PlotType::ProgressBar { value, total });
    }

    pub fn clear(&self, plot_name: &str) {
        self.rod.clear_blocking(plot_name);
    }
}

#[pymodule]
fn plotfish(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PythonFishingRod>()?;
    Ok(())
}

// Javascript bindings

struct JavascriptFishingRod {}

impl JavascriptFishingRod {
    fn new(mut cx: FunctionContext) -> JsResult<JsBox<FishingRod>> {
        let riverbed_url = cx.argument::<JsString>(0)?.value(&mut cx);
        let api_key = cx.argument::<JsString>(1)?.value(&mut cx);

        let rod = FishingRod::new(riverbed_url, api_key);
        Ok(cx.boxed(rod))
    }

    fn line(mut cx: FunctionContext) -> JsResult<JsUndefined> {
        let plot_name = cx.argument::<JsString>(0)?.value(&mut cx);
        let value = cx.argument::<JsNumber>(1)?.value(&mut cx);

        cx.this()
            .downcast_or_throw::<JsBox<FishingRod>, _>(&mut cx)
            .unwrap()
            .record_datapoint_blocking(plot_name, PlotType::Line { value });

        Ok(cx.undefined())
    }

    fn counter(mut cx: FunctionContext) -> JsResult<JsUndefined> {
        let plot_name = cx.argument::<JsString>(0)?.value(&mut cx);
        let change = cx.argument::<JsNumber>(1)?.value(&mut cx);

        cx.this()
            .downcast_or_throw::<JsBox<FishingRod>, _>(&mut cx)
            .unwrap()
            .record_datapoint_blocking(plot_name, PlotType::Counter { change });

        Ok(cx.undefined())
    }

    fn progress_bar(mut cx: FunctionContext) -> JsResult<JsUndefined> {
        let plot_name = cx.argument::<JsString>(0)?.value(&mut cx);
        let value = cx.argument::<JsNumber>(1)?.value(&mut cx);
        let total = cx.argument::<JsNumber>(2)?.value(&mut cx);

        cx.this()
            .downcast_or_throw::<JsBox<FishingRod>, _>(&mut cx)
            .unwrap()
            .record_datapoint_blocking(plot_name, PlotType::ProgressBar { value, total });

        Ok(cx.undefined())
    }
}

#[neon::main]
fn main(mut cx: ModuleContext) -> NeonResult<()> {
    cx.export_function("fishingRodNew", JavascriptFishingRod::new)?;
    cx.export_function("fishingRodLine", JavascriptFishingRod::line)?;
    cx.export_function("fishingRodCounter", JavascriptFishingRod::counter)?;
    cx.export_function("fishingRodProgressBar", JavascriptFishingRod::progress_bar)?;
    Ok(())
}
