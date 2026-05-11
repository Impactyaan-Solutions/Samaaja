import { getAPIToken, getRequestOptions } from '../auth'

// For local dev, use relative paths to hit the Vite proxy (fixes CORS/Cookies)
// For production (Capacitor/Web), use the absolute URL
const baseurl = import.meta.env.DEV ? '' : import.meta.env.VITE_API_BASE_URL

export const getFeed = async () => {
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    const requestOptions = getRequestOptions()
    const response = await fetch(
        baseurl + '/api/method/samaaja.api.feed.get_feed',
        { ...requestOptions, headers }
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
    const requestOptions = getRequestOptions()

    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    const params = new URLSearchParams({ user_email: email })
    const url = `${baseurl}/api/method/samaaja.api.user.user_profile?${params.toString()}`

    const response = await fetch(url, {
        headers,
        ...requestOptions
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

export const getLoggedUser = async () => {
    const requestOptions = getRequestOptions()
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        ...requestOptions.headers
    }
    const response = await fetch(
        baseurl + '/api/method/frappe.auth.get_logged_user',
        { ...requestOptions, headers }
    )
    if (response.ok) {
        const result = await response.json();
        const data = result.message
        return data
    } else {
        throw new Error('Failed to fetch user')
    }
}

export const getGoogleSignInURL = async () => {
    const response = await fetch(baseurl + '/api/method/samaaja.api.login.get_google_auth_url', {
        method: 'GET',
        headers: {
            'Accept': 'application/json'
        }
    });
    if (!response.ok) {
        const errorText = await response.text();
        console.error("Server Error Output:", errorText);
        throw new Error(`Server error: ${response.status}`);
    }

    const result = await response.json();
    return result.message
}

export const fetchImageAsBase64 = async (url) => {
    try {
        // Rewrite absolute URLs to relative paths in DEV so Vite proxy can handle CORS
        if (import.meta.env.DEV && url.startsWith('http')) {
            try {
                const urlObj = new URL(url);
                url = urlObj.pathname + urlObj.search;
            } catch (e) {
                // Ignore invalid URLs
            }
        }

        const response = await fetch(url, getRequestOptions());
        if (!response.ok) throw new Error('Network response was not ok');
        const blob = await response.blob();
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsDataURL(blob);
        });
    } catch (error) {
        console.error("Failed to fetch image as base64", error);
        return null;
    }
}

export const updateUserProfile = async (data) => {
    // Note: The endpoint `samaaja.api.user.update_profile` is a placeholder. 
    // You will need to replace this with the exact endpoint provided by your backend team.
    const url = `${baseurl}/api/method/samaaja.api.user.update_profile`

    const requestOptions = getRequestOptions()
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    const response = await fetch(url, {
        method: 'POST',
        headers,
        ...requestOptions,
        body: JSON.stringify(data)
    })

    if (!response.ok) {
        throw new Error(`Failed to update profile: ${response.statusText}`)
    }

    const result = await response.json()
    return result.message || result.data
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