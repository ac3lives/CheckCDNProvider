import getCloudflare, getCloudfront, getMerlinCDN


def build_cdn_list():
        cdnProviders = ['cloudflare', 'cloudfront', 'merlin']
        providerIPRanges = [getCloudflare.get_cloudflare_cdn_ranges(), getCloudfront.get_cloudfront_cdn_ranges(), getMerlinCDN.get_merlin_cdn_ranges()]
        return dict(zip(cdnProviders, providerIPRanges))

if __name__ == '__main__':
        print(build_cdn_list())