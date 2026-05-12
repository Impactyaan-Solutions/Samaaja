import { getAPIToken, getRequestOptions } from '../auth'
import imageCompression from 'browser-image-compression'

// For local dev, use relative paths to hit the Vite proxy (fixes CORS/Cookies)
// For production (Capacitor/Web), use the absolute URL
const baseurl = import.meta.env.DEV ? '' : import.meta.env.VITE_API_BASE_URL

export const getFeed = async (limit = 10, offset = 0) => {
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    const requestOptions = getRequestOptions()
    const response = await fetch(
        `${baseurl}/api/method/samaaja.api.feed.get?limit=${limit}&offset=${offset}`,
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
export const logout = async () => {
    const requestOptions = getRequestOptions();

    // Changing to GET often bypasses CSRF issues on logout
    const response = await fetch(baseurl + '/api/method/logout', {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            ...requestOptions.headers
        },
        ...requestOptions
    });

    // We don't strictly throw an error here because if the logout fails 
    // on the server, we still want the user to be logged out locally.
    return response.ok;
};

export const completeProfile = async (data) => {
    const requestOptions = getRequestOptions()
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    const response = await fetch(baseurl + '/api/method/samaaja.api.user.complete_user_profile', {
        method: 'POST',
        headers,
        ...requestOptions,
        body: JSON.stringify(data)
    })

    if (!response.ok) {
        throw new Error(`Failed to complete profile: ${response.statusText}`)
    }

    const result = await response.json()
    return result.message || result.data
}

export const createAccount = async (data) => {
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    const response = await fetch(baseurl + '/api/method/samaaja.api.user.create_user', {
        method: 'POST',
        headers,
        body: JSON.stringify(data)
    })

    if (!response.ok) {
        throw new Error(`Failed to complete profile: ${response.statusText}`)
    }

    const result = await response.json()
    return result.message || result.data
}

export const loginUsingOtp = async (data) => {
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    const response = await fetch(baseurl + '/api/method/samaaja.api.login.login_using_otp', {
        method: 'POST',
        headers,
        body: JSON.stringify(data)
    })


    if (response.status === 404) {
        alert("User not found!")
        return false
    }
    if (!response.ok) {
        throw new Error(`Failed to verify otp and login: ${response.statusText}`)
    }
    return true
}

export const logAction = async (data) => {
    try {
        console.log("ORIGINAL DATA", data)

        const formData = new FormData()

        for (const key in data) {

            // Handle file arrays
            if (Array.isArray(data[key])) {

                for (const item of data[key]) {

                    if (item.file instanceof File) {

                        console.log("Compressing:", item.file.name)

                        const compressedFile = await imageCompression(
                            item.file,
                            {
                                maxSizeMB: 0.25,
                                maxWidthOrHeight: 1280,
                                initialQuality: 0.6,
                                useWebWorker: true,
                            }
                        )

                        console.log(
                            `Compressed ${item.file.size / 1024} KB → ${compressedFile.size / 1024} KB`
                        )

                        formData.append(
                            key,
                            compressedFile,
                            compressedFile.name
                        )
                    }
                }

            } else {

                // Skip null/undefined
                if (data[key] !== null && data[key] !== undefined) {
                    formData.append(key, data[key])
                }
            }
        }

        console.log("FORM DATA READY")

        const response = await fetch(
            baseurl + '/api/method/samaaja.api.action.create',
            {
                method: 'POST',
                credentials: 'include',
                body: formData
            }
        )

        console.log("RESPONSE RECEIVED", response)

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`)
        }

        const result = await response.json()

        console.log("RESULT", result)

        return result

    } catch (err) {

        console.error("FETCH FAILED", err)

        throw err
    }
}


export const addPost = async (data) => {
    try {
        console.log("ORIGINAL DATA", data)

        const formData = new FormData()

        for (const key in data) {

            // Handle file arrays
            if (Array.isArray(data[key])) {

                for (const item of data[key]) {

                    if (item.file instanceof File) {

                        console.log("Compressing:", item.file.name)

                        const compressedFile = await imageCompression(
                            item.file,
                            {
                                maxSizeMB: 0.25,
                                maxWidthOrHeight: 1280,
                                initialQuality: 0.6,
                                useWebWorker: true,
                            }
                        )

                        console.log(
                            `Compressed ${item.file.size / 1024} KB → ${compressedFile.size / 1024} KB`
                        )

                        formData.append(
                            key,
                            compressedFile,
                            compressedFile.name
                        )
                    }
                }

            } else {

                // Skip null/undefined
                if (data[key] !== null && data[key] !== undefined) {
                    formData.append(key, data[key])
                }
            }
        }

        console.log("FORM DATA READY")

        const response = await fetch(
            baseurl + '/api/method/samaaja.api.post.add',
            {
                method: 'POST',
                credentials: 'include',
                body: formData
            }
        )

        console.log("RESPONSE RECEIVED", response)

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`)
        }

        const result = await response.json()

        console.log("RESULT", result)

        return result

    } catch (err) {

        console.error("FETCH FAILED", err)

        throw err
    }
}