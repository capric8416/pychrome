(function () {
    var proxy = ''


    function set_proxy(url) {
        url = new URL(url)

        let proxy = {
            scope: url.searchParams.get('scope'),
            value: {
                mode: 'fixed_servers',
                rules: {
                    singleProxy: {
                        scheme: url.searchParams.get('scheme'),
                        host: url.searchParams.get('host'),
                        port: parseInt(url.searchParams.get('port'))
                    },
                    bypassList: ['127.0.0.1', 'localhost', 'http:://127.0.0.1', 'http://localhost']
                }
            }
        }

        chrome.proxy.settings.set(proxy, function () { })
    }


    chrome.webRequest.onSendHeaders.addListener(
        function (details) {
            if (details.url.includes('http://localhost/proxy/change/') && details.type === 'main_frame' && details.url !== proxy) {
                proxy = details.url
                alert(proxy)
                set_proxy(proxy)
            }
        },
        { urls: ['<all_urls>'] }
    )


    chrome.webRequest.onBeforeRequest.addListener(
        function (details) {
            if (details.type === 'stylesheet') {
                return { cancel: true }
            }
        },
        { urls: ['<all_urls>'] },
        ['blocking']
    )


    document.addEventListener('DOMContentLoaded', function () {
        chrome.contentSettings.images.set({
            'scope': 'regular',
            'setting': 'block',
            'primaryPattern': '<all_urls>',
        });
    });


})();