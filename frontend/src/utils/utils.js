import i18n from '@/i18n' // Ensure this path matches your i18n.js file location

export const getTimeSinceCreation = (creationDate) => {
    // Access the global translate function
    const { t } = i18n.global;
    
    const now = new Date();
    const creation = new Date(creationDate);
    const diff = now - creation;
    
    // Calculate units
    const minutes = Math.floor(diff / (1000 * 60));
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));

    if (days >= 1) {
        return t('time_ago.days', { n: days });
    }
    
    if (hours >= 1) {
        return t('time_ago.hours', { n: hours });
    }
    
    if (minutes >= 1) {
        return t('time_ago.minutes', { n: minutes });
    }

    return t('time_ago.just_now');
}