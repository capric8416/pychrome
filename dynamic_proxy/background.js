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
    function (har_entry) {
        if (har_entry.url.includes('http://localhost/proxy/change/') && har_entry.type === 'main_frame') {
            set_proxy(har_entry.url)
        }
    },
    { urls: ['<all_urls>'] }
)
