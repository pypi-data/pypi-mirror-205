"use strict";

// TODO: figure out how to package Rust binary? Seems like we have to include the binary
// https://github.com/neon-bindings/neon/issues/960
// https://github.com/neon-bindings/neon/issues/117
// https://github.com/prebuild/prebuildify + https://github.com/prebuild/node-gyp-build ?
// https://github.com/mapbox/node-pre-gyp

const { fishingRodNew, fishingRodLine, fishingRodCounter, fishingRodProgressBar } = require("./index.node");

// TODO: convert to Typescript
class Plotfish {
    constructor(apiKey, riverbedUrl = 'http://localhost:8000') {
        this.rod = fishingRodNew(riverbedUrl, apiKey);
    }

    line(plotName, value) {
        fishingRodLine.call(this.rod, plotName, value);
    }


    counter(plotName, change) {
        fishingRodCounter.call(this.rod, plotName, change);
    }


    progressBar(plotName, value, total) {
        fishingRodProgressBar.call(this.rod, plotName, value, total);
    }
}


module.exports = Plotfish;