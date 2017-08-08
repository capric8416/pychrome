function set_proxy(url) {
    url = new URL(url)

    let scope = url.searchParams.get('scope')

    // let proxy = url.searchParams.get('value').replace('http://', '').split(':')
    // let host = proxy[0]
    // let port = parseInt(proxy[1])
    let proxy = url.searchParams.get('value')


    // let value = {
    //     mode: 'fixed_servers',
    //     rules: {
    //         singleProxy: {
    //             scheme: 'http',
    //             host: host,
    //             port: port
    //         }
    //     },
    //     bypassList: ['localhost', '127.0.0.1']
    // }

    let value = {
        mode: 'pac_script',
        pacScript: {
            data: `function FindProxyForURL(url, host) {
                if (host == '127.0.0.1' || host == 'localhost') {
                    return 'DIRECT'
                }
                return 'PROXY ${proxy}'
            }`
        }
    }


    chrome.proxy.settings.set(
        { value: value, scope: scope },
        function () {
            // chrome.proxy.settings.get(
            //     { incognito: true },
            //     function (details) {
            //     }
            // )
        }
    )
}



chrome.webRequest.onSendHeaders.addListener(
    function (har_entry) {
        if (har_entry.url.includes('http://localhost/proxy/change/') && har_entry.type === 'main_frame') {
            set_proxy(har_entry.url)
        }
    },
    { urls: ['<all_urls>'] }
)



chrome.proxy.onProxyError.addListener(function (details) {
})
