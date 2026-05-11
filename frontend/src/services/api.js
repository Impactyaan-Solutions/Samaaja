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
export const getProfile = async (email) => {
    const baseurl = import.meta.env.VITE_API_BASE_URL
    const requestOption = getRequestOptions()
    
    // Merge headers to keep the API key and set JSON types
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        ...requestOption.headers 
    }

    const params = new URLSearchParams({ user_email: email })
    const url = `${baseurl}/api/method/samaaja.api.user.user_profile?${params.toString()}`

    const response = await fetch(url, {
        ...requestOption,
        headers
    })

    if (response.ok) {
        const result = await response.json()
        console.log("API Response:", result) // Debugging log
        // Returns the message object from Frappe
        return result.data
    } else {
        throw new Error(`Profile fetch failed: ${response.statusText}`)
    }
}

export const getLeaderboard = async () => {
    const requestOption = getRequestOptions()
    
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        ...requestOption.headers
    }

    const url = `${baseurl}/api/method/samaaja.api.leaderboard.user_leaderboard`

    const response = await fetch(url, {
        ...requestOption,
        headers
    })

    if (response.ok) {
        const result = await response.json()
        // Returning result.data to stay consistent with your other methods
        return result.data
        console.log("Leaderboard API Response:", result) // Debugging log
    } else {
        throw new Error(`Leaderboard fetch failed: ${response.statusText}`)
        
    }
}