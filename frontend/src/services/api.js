import { getAPITokenFromStorage, getRequestOptions } from '../auth'
import imageCompression from 'browser-image-compression'
import { Capacitor } from '@capacitor/core'
import { CapacitorCookies } from '@capacitor/core'

// The app is served by the same Frappe site it talks to, so every request
// is relative.
//
// ANDROID BUILD: this must not stay empty on a phone. A native app has no
// "same site" to call, so it needs the full server address instead:
//
//     const baseurl = Capacitor.isNativePlatform()
//       ? import.meta.env.VITE_API_BASE_URL
//       : ''
//
// That is one of three changes the mobile build needs - see the Android
// notes in Step 2 for the vite.config.js build mode and the allow_cors
// setting on the server.
const baseurl = ''

export const getFeed = async (limit = 10, offset = 0) => {
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    const response = await callAPI(headers, `${baseurl}/api/method/samaaja.api.feed.get?limit=${limit}&offset=${offset}`, 'GET', null)
    return response.data
}

export const unlikePost = async (post_id, user_id) => {
    try {
        const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        const result = await callAPI(headers, baseurl + '/api/method/samaaja.api.post.unlike', 'POST', { post_id, user_id })
        return result.data
    }
    catch (err) {
        console.error("FETCH FAILED", err)
        throw err
    }
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

export const getLoginOptions = async () => {
    const response = await fetch(baseurl + '/api/method/samaaja.api.login.get_login_options', {
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

export const getBranding = async () => {
    const response = await fetch(baseurl + '/api/method/samaaja.api.settings.get_branding', {
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
    const headers = {
        'Accept': 'application/json',
    }
    await callAPI(headers, baseurl + '/api/method/logout', 'POST')
    return true;
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

export const loginUsingPassword = async (data) => {
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    const response = await fetch(baseurl + '/api/method/samaaja.api.login.login_using_password', {
        method: 'POST',
        headers,
        body: JSON.stringify(data)
    })

    if (response.status === 404) {
        alert("User not found!")
        return false
    }
    if (!response.ok) {
        throw new Error(`Failed to verify password and login: ${response.statusText}`)
    }

    if (Capacitor.isNativePlatform()) {

        const data = await response.json()

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

export const loginWithUsernamePassword = async (usr, pwd) => {
    // This core endpoint takes form-encoded data, unlike every other
    // endpoint in this file which takes JSON.
    const body = new URLSearchParams({ usr, pwd })

    const response = await fetch(baseurl + '/api/method/login', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body
    })

    if (!response.ok) {
        throw new Error('Invalid email or password')
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


const SEEN_ANNOUNCEMENTS_KEY = 'samaaja_seen_announcements'

const getSeenAnnouncements = () => {
    try { return JSON.parse(localStorage.getItem(SEEN_ANNOUNCEMENTS_KEY) || '[]') } catch { return [] }
}

/* const markAnnouncementSeen = (name) => {
    const seen = getSeenAnnouncements()
    if (!seen.includes(name)) {
        seen.push(name)
        localStorage.setItem(SEEN_ANNOUNCEMENTS_KEY, JSON.stringify(seen))
    }
} */

export const getActiveAnnouncements = async () => {
    const headers = { 'Accept': 'application/json', 'Content-Type': 'application/json' }
    const result = await callAPI(headers, `${baseurl}/api/method/samaaja.api.announcements.get_active_announcements`, 'GET', null)
    return result.data
}

export const getVolunteerListings = async (
    filters = {},
    limit = 10,
    offset = 0
) => {
    try {
        const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        const params = new URLSearchParams({
            filters: JSON.stringify(filters),
            limit: String(limit),
            offset: String(offset)
        })

        const result = await callAPI(
            headers,
            `${baseurl}/api/method/samaaja.api.volunteer.get_list?${params.toString()}`,
            'GET',
            null
        )

        if (Array.isArray(result?.data?.opportunities)) {
            return {
                opportunities: result.data.opportunities,
                has_more: result.data.has_more,
                limit: result.data.limit,
                offset: result.data.offset
            }
        }

        if (Array.isArray(result?.message?.data?.opportunities)) {
            return {
                opportunities: result.message.data.opportunities,
                has_more: result.message.data.has_more,
                limit: result.message.data.limit,
                offset: result.message.data.offset
            }
        }

        return {
            opportunities: [],
            has_more: false,
            limit,
            offset
        }
    } catch (error) {
        console.warn('Failed to fetch volunteer listings.', error)
        throw error
    }
}

export const createVolunteerInterest = async ({ user, volunteer_opportunity }) => {
    const headers = { 'Accept': 'application/json', 'Content-Type': 'application/json' }
    const url = `${baseurl}/api/resource/Volunteer%20Interest`

    const result = await callAPI(headers, url, 'POST', {
        user,
        volunteer_opportunity
    })

    return result.data || result
}

/* export const getLocalUnreadCount = async () => {
    const announcements = await getActiveAnnouncements()
    const seen = getSeenAnnouncements()
    if (seen.length === 0) {
        return announcements.length
    }
    return announcements.filter(a => !seen.includes(a.name)).length
}

export const recordInteraction = async (announcement, type, contactId = null) => {
    if (type === 'View') markAnnouncementSeen(announcement)
    return await callAPI(
        {},
        `${baseurl}/api/method/samaaja.api.announcements.record_interaction`,
        'POST',
        new URLSearchParams({ announcement, interaction_type: type, contact_id: contactId || '' }),
        true
    )
} */

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
// Methods that change data. Frappe only demands a CSRF token for these;
// GET and HEAD are waved through.
const UNSAFE_METHODS = ['POST', 'PUT', 'DELETE', 'PATCH']

// Now that the app is served by Frappe itself, the browser attaches the
// session cookie to every request. Frappe therefore sees a real logged-in
// session and requires a CSRF token on any write, or it answers 400
// "Invalid Request".
//
// The token is put on the page by samaaja/www/index.html, which Frappe
// renders through Jinja before serving it. It is per-session, which is why
// that page must never be cached (see no_cache in www/index.py).
//
// This did not arise before the move: the app was on another origin, the
// cookie was never sent, and Frappe skipped the check because the session
// held no token.
const csrfHeader = (method) => {
    if (!UNSAFE_METHODS.includes(String(method).toUpperCase())) return {}
    const token = typeof window !== 'undefined' && window.csrf_token
    return token ? { 'X-Frappe-CSRF-Token': token } : {}
}

const callAPI = async (headers, url, method, data = null, isFormData = false, addToken = true) => {

    if (Capacitor.isNativePlatform() && addToken) {
        headers = { ...headers, ...getAPITokenFromStorage() }
    } else {
        headers = { ...headers, ...getRequestOptions(), ...csrfHeader(method) }
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
export const createComment = async (post_id, comment_text) => {
    try {
        const headers = {   
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        const result = await callAPI(
            headers,
            baseurl + '/api/method/samaaja.api.comment.create',
            'POST',
            {
                post_id,
                comment_text
            }
        )

        return result.data
    } catch (err) {
        console.error("CREATE COMMENT FAILED", err)
        throw err
    }
}

export const getComments = async (post_id) => {
    try {
        const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        const result = await callAPI(
            headers,
            `${baseurl}/api/method/samaaja.api.comment.get?post_id=${post_id}`,
            'GET',
            null
        )

        return result.data
    } catch (err) {
        console.error("GET COMMENTS FAILED", err)
        throw err
    }
}

export const getUserProfilePosts = async (user,limit = 10, offset = 0) => {
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    const response = await callAPI(headers, `${baseurl}/api/method/samaaja.api.profile.get_posts?user=${user}&limit=${limit}&offset=${offset}`, 'GET', null)
    return response.data
}
export const getUserProfileActions = async (user,limit = 10, offset = 0) => {
     const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    const response = await callAPI(headers, `${baseurl}/api/method/samaaja.api.profile.get_actions?user=${user}&limit=${limit}&offset=${offset}`, 'GET', null)
    return response.data
}
// --- Volunteer and metadata endpoints, ported from samaaja_frontend (fe/main).
//     They go through callAPI above, so csrfHeader() adds X-Frappe-CSRF-Token
//     on unsafe methods without any change here.

export const getVolunteerOpportunity = async (volunteerId) => {
    try {
        const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        const params = new URLSearchParams({
            volunteer_id: volunteerId
        })

        const result = await callAPI(
            headers,
            `${baseurl}/api/method/samaaja.api.volunteer.get?${params.toString()}`,
            'GET',
            null
        )

        if (result?.data?.opportunity) {
            return result.data.opportunity
        }

        if (result?.message?.data?.opportunity) {
            return result.message.data.opportunity
        }

        throw new Error('Volunteer opportunity data not found')
    } catch (error) {
        console.error('Failed to fetch volunteer opportunity:', error)
        throw error
    }
}

export const checkVolunteerApplication = async (volunteerId) => {
    try {
        const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        const params = new URLSearchParams({
            volunteer_opportunity: volunteerId
        })

        const result = await callAPI(
            headers,
            `${baseurl}/api/method/samaaja.api.volunteer.check_application?${params.toString()}`,
            'GET',
            null
        )

        return result.data || result.message?.data || result
    } catch (error) {
        console.error('Failed to check volunteer application:', error)
        throw error
    }
}

export const applyForVolunteerOpportunity = async (applicationData) => {
    try {
        const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        const result = await callAPI(
            headers,
            `${baseurl}/api/method/samaaja.api.volunteer.apply`,
            'POST',
            applicationData
        )

        return result.data || result.message?.data || result
    } catch (error) {
        console.error('Failed to apply for volunteer opportunity:', error)
        throw error
    }
}

export const getMetadataOptions = async (doctype) => {
    try {
        const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        const params = new URLSearchParams({
            doctype
        })

        const result = await callAPI(
            headers,
            `${baseurl}/api/method/samaaja.api.metadata.get_list?${params.toString()}`,
            'GET',
            null
        )

        return result?.data || result?.message?.data || []
    } catch (error) {
        console.error(`Failed to fetch metadata options for ${doctype}:`, error)
        throw error
    }
}
