import { getAPITokenFromStorage, getRequestOptions } from '../auth'
import imageCompression from 'browser-image-compression'
import { Capacitor } from '@capacitor/core'
import { CapacitorCookies } from '@capacitor/core'

// For local dev, use relative paths to hit the Vite proxy (fixes CORS/Cookies)
// For production (Capacitor/Web), use the absolute URL
const baseurl = import.meta.env.DEV ? '' : import.meta.env.VITE_API_BASE_URL

export const getFeed = async (limit = 10, offset = 0) => {
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    const response = await callAPI(headers, `${baseurl}/api/method/samaaja.api.feed.get?limit=${limit}&offset=${offset}`, 'GET', null)
    return response.data
}
export const getProfile = async (email) => {
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    const params = new URLSearchParams({ user_email: email })
    const url = `${baseurl}/api/method/samaaja.api.user.user_profile?${params.toString()}`

    const data = await callAPI(headers, url, 'GET', null)

    // Returns the message object from Frappe
    return data.data
}

export const getLoggedUser = async () => {
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    const data = await callAPI(headers, baseurl + '/api/method/frappe.auth.get_logged_user', 'GET', null)
    return data.message

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
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    const url = `${baseurl}/api/method/samaaja.api.leaderboard.user_leaderboard`

    const data = await callAPI(headers, url, 'GET', null)

    // Returning result.data to stay consistent with your other methods
    return data.data
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
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    const result = await callAPI(headers, baseurl + '/api/method/samaaja.api.user.complete_user_profile', 'POST', data)
    return result.data
}

export const createAccount = async (data) => {
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    const result = await callAPI(headers, baseurl + '/api/method/samaaja.api.user.create_user', 'POST', data, false, false)
    return result.data
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

    if (Capacitor.isNativePlatform()) {

        const data = await response.json()

        console.log("LOGIN RESPONSE", data.data)

        // Store user auth tokens
        localStorage.setItem(
            'api_key',
            data.data.api_key
        )

        localStorage.setItem(
            'api_secret',
            data.data.api_secret
        )

        localStorage.setItem(
            'user',
            data.data.user
        )
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
        const result = await callAPI({}, baseurl + '/api/method/samaaja.api.action.create', 'POST', formData, true)
        return result.data

    }
    catch (err) {

        console.error("FETCH FAILED", err)

        throw err
    }
}


export const getActiveAnnouncements = async () => {
    const headers = { 'Accept': 'application/json', 'Content-Type': 'application/json' }
    const result = await callAPI(headers, `${baseurl}/api/method/samaaja_announcements.samaaja_announcements.api.get_active_announcements`, 'GET', null)
    return result.message
}

export const getUnreadCount = async () => {
    try {
        const headers = { 'Accept': 'application/json', 'Content-Type': 'application/json' }
        const result = await callAPI(headers, `${baseurl}/api/method/samaaja_announcements.samaaja_announcements.api.get_unread_count`, 'GET', null)
        return result.message
    } catch {
        return 0
    }
}

export const recordInteraction = async (announcement, type, contactId = null) => {
    return await callAPI(
        {},
        `${baseurl}/api/method/samaaja_announcements.samaaja_announcements.api.record_interaction`,
        'POST',
        new URLSearchParams({ announcement, interaction_type: type, contact_id: contactId || '' }),
        true
    )
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
        const result = await callAPI({}, baseurl + '/api/method/samaaja.api.post.add', 'POST', formData, true)
        return result.data

    } catch (err) {

        console.error("FETCH FAILED", err)

        throw err
    }
}

export const likePost = async (post_id, user_id) => {
    try {
        const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        const result = await callAPI(headers, baseurl + '/api/method/samaaja.api.post.like', 'POST', { post_id, user_id })
        return result.data
    }
    catch (err) {
        console.error("FETCH FAILED", err)
        throw err
    }
}
const callAPI = async (headers, url, method, data = null, isFormData = false, addToken = true) => {

    if (Capacitor.isNativePlatform() && addToken) {
        headers = { ...headers, ...getAPITokenFromStorage() }
    } else {
        headers = { ...headers, ...getRequestOptions() }
    }
    console.log(headers)
    let response
    if (data != null) {
        if (isFormData) {
            response = await fetch(url, {
                method: method,
                headers: headers,
                body: data
            })
        } else {
            response = await fetch(url, {
                method: method,
                headers: headers,
                body: JSON.stringify(data)
            })
        }
    } else {
        response = await fetch(url, {
            method: method,
            headers: headers
        })
    }

    if (response.ok) {
        const result = await response.json();
        return result
    } else {
        const data = await response.json()
        throw new Error(data.message)
    }
}