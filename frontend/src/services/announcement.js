export const getActiveAnnouncements = async () => {
    const response = await fetch(
        '/api/method/samaaja_announcements.samaaja_announcements.api.get_active_announcements'
    )
    if (response.ok) {
        const result = await response.json();
        return result.message
    } else {
        throw new Error('Failed to fetch announcements')
    }
}

export const getUnreadCount = async () => {
    const response = await fetch(
        '/api/method/samaaja_announcements.samaaja_announcements.api.get_unread_count'
    )
    if (response.ok) {
        const result = await response.json();
        return result.message
    } else {
        return 0
    }
}

export const recordInteraction = async (announcement, type, contactId = null) => {
    const response = await fetch(
        '/api/method/samaaja_announcements.samaaja_announcements.api.record_interaction',
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                announcement: announcement,
                interaction_type: type,
                contact_id: contactId || ''
            })
        }
    )
    return await response.json()
}
