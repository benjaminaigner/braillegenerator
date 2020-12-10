self.addEventListener('message', function (e) {
    if (e.data && e.data.cmd == 'render') {
        if (e.data.baselibraries && e.data.libraries) {
            importScripts.apply(null, e.data.baselibraries.concat(e.data.libraries));
        }
        e.data.script += 'this.main = main;';
        var f = new Function(e.data.script);
        f.apply(self, []);
        OpenJsCad.runMainInWorker(e.data.parameters);
    }
}, false);