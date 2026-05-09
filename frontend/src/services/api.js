import { getRequestOptions } from '../auth'

const baseurl = import.meta.env.VITE_API_BASE_URL

export const getFeed = async () => {
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    const requestOption = getRequestOptions()
    const response = await fetch(
        baseurl + '/api/method/samaaja.api.feed.get_feed',
        { ...requestOption, headers }
    )
    if (response.ok) {
        const result = await response.json();
        const feed = result.data
        return feed
    } else {
        throw new Error('Failed to fetch feed')
    }
}