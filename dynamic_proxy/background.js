(function () {
    var last_proxy_url = ''


    function validate(s) {
        return s !== undefined && s !== null && s !== ''
    }


    function set_proxy(url) {
        last_proxy_url = url

        url = new URL(url)

        let scope = url.searchParams.get('scope')
        let scheme = url.searchParams.get('scheme')
        let host = url.searchParams.get('host')
        let port = url.searchParams.get('port')

        let proxy = {
            scope: 'regular',
            value: {
                mode: 'direct'
            }
        }
        if (validate(scope) && validate(scheme) && validate(host) && validate(port)) {
            proxy = {
                scope: scope,
                value: {
                    mode: 'fixed_servers',
                    rules: {
                        singleProxy: {
                            scheme: scheme,
                            host: host,
                            port: parseInt(port)
                        },
                        bypassList: ['127.0.0.1', 'localhost', 'http:://127.0.0.1', 'http://localhost']
                    }
                }
            }
        }

        chrome.proxy.settings.set(proxy, function () { })
    }


    function remove_browsing_data() {
        chrome.browsingData.remove(
            {
                'since': 0,
                'originTypes': {
                    'protectedWeb': true,
                    'unprotectedWeb': true
                }
            },
            {
                'appcache': true,
                'cache': true,
                'cookies': true,
                'downloads': true,
                'fileSystems': true,
                'formData': true,
                'history': true,
                'indexedDB': true,
                'localStorage': true,
                'passwords': true,
                'pluginData': true,
                'serviceWorkers': true,
                'webSQL': true
            },
            function () { }
        )
    }


    function disable_image() {
        chrome.contentSettings.images.set({
            'scope': 'regular',
            'setting': 'block',
            'primaryPattern': '<all_urls>',
        });
    }


    function enable_image() {
        chrome.contentSettings.images.set({
            'scope': 'regular',
            'setting': 'allow',
            'primaryPattern': '<all_urls>',
        });
    }


    function cancel_stylesheet_request(details) {
        if (details.type === 'stylesheet') {
            return { cancel: true }
        }
    }


    function disable_stylesheet() {
        if (!chrome.webRequest.onBeforeRequest.hasListener(cancel_stylesheet_request)) {
            chrome.webRequest.onBeforeRequest.addListener(
                cancel_stylesheet_request,
                { urls: ['<all_urls>'] },
                ['blocking']
            )
        }
    }


    function enable_stylesheet() {
        if (chrome.webRequest.onBeforeRequest.hasListener(cancel_stylesheet_request)) {
            chrome.webRequest.onBeforeRequest.removeListener(cancel_stylesheet_request)
        }
    }


    function batch_actions(url) {
        url = new URL(url)

        let browsing_data = url.searchParams.get('browsing_data')
        if (validate(browsing_data)) {
            remove_browsing_data()
        }

        let image = url.searchParams.get('image')
        if (validate(image)) {
            if (image === 'enable') {
                enable_image()
            }
            else if (image === 'disable') {
                disable_image()
            }
        }

        let stylesheet = url.searchParams.get('stylesheet')
        if (validate(stylesheet)) {
            if (stylesheet === 'enable') {
                enable_stylesheet()
            }
            else if (stylesheet === 'disable') {
                disable_stylesheet()
            }
        }

        let proxy = url.searchParams.get('proxy')
        if (validate(proxy)) {
            proxy = proxy.split('|')
            let url = `http://localhost/proxy/change/?scope=${proxy[0]}&scheme=${proxy[1]}&host=${proxy[2]}&port=${proxy[3]}`
            set_proxy(url)
        }
    }


    function map_url_function(details) {
        if (details.type === 'main_frame') {
            if (details.url.includes('http://localhost/batch/actions/')) {
                batch_actions(details.url)
            }
            else if (details.url.includes('http://localhost/image/enable/')) {
                enable_image()
            }
            else if (details.url.includes('http://localhost/image/disable/')) {
                disable_image()
            }
            else if (details.url.includes('http://localhost/stylesheet/enable/')) {
                enable_stylesheet()
            }
            else if (details.url.includes('http://localhost/stylesheet/disable/')) {
                disable_stylesheet()
            }
            else if (details.url.includes('http://localhost/browsing_data/remove/')) {
                remove_browsing_data()
            }
            else if (details.url.includes('http://localhost/proxy/change/') && details.url !== last_proxy_url) {
                set_proxy(details.url)
            }
        }
    }


    chrome.webRequest.onSendHeaders.addListener(
        map_url_function,
        { urls: ['<all_urls>'] }
    )

})();

