export const getTimeSinceCreation = (creationDate) => {
    const now = new Date();
    const creation = new Date(creationDate);
    const diff = now - creation;
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    if (days === 0) {
        const hours = Math.floor(diff / (1000 * 60 * 60));
        if (hours === 0) {
            const minutes = Math.floor(diff / (1000 * 60));
            if (minutes === 0) {
                return 'Just now';
            }
            return minutes + ' minutes ago';
        }
        return hours + ' hours ago';
    }

    return days + ' days ago';
}