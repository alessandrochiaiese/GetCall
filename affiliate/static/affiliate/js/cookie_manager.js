
function setAffiliateCookie(name, value, days) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = "expires=" + date.toUTCString();
    document.cookie = name + "=" + value + ";" + expires + ";path=/";
}

// Verifica se il parametro di affiliazione è presente nell'URL
const urlParams = new URLSearchParams(window.location.search);
const affiliateId = urlParams.get('affiliate_id');
const programId = urlParams.get('program_id');

if (affiliateId && programId) {
    setAffiliateCookie('affiliate_id', affiliateId, 30); // Cookie valido per 30 giorni
    setAffiliateCookie('program_id', programId, 30);
}