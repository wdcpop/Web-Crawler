export function formatTime(ts) {
    const date = new Date(ts);
    const year = date.getFullYear();
    const month = parseInt(date.getMonth()) + 1;
    const day = date.getDate();
    let minute = date.getMinutes();
    const hour = date.getHours();
    if (parseInt(minute) < 10) {
        minute = '0' + minute;
    }
    return year + '-' + month + '-' + day + ' ' + hour + ':' + minute;
}

export function formatTimeSlash(ts) {
    const date = new Date(ts);
    const year = date.getFullYear();
    let month = parseInt(date.getMonth()) + 1;
    let day = date.getDate();
    let minute = date.getMinutes();
    const hour = date.getHours();
    if (parseInt(minute) < 10) {
        minute = '0' + minute;
    }
    if(month < 10) month = `0${month}`
    if(day < 10) day = `0${day}`
    return year + '' + month + '' + day
}

export function formatTimeWithSymbol(ts, symbol) {
    const date = new Date(ts);
    const year = date.getFullYear();
    let month = parseInt(date.getMonth()) + 1;
    let day = date.getDate();
    let minute = date.getMinutes();
    const hour = date.getHours();
    if (parseInt(minute) < 10) {
        minute = '0' + minute;
    }
    if(month < 10) month = `0${month}`
    if(day < 10) day = `0${day}`
    return year + symbol + month + symbol + day
}

export function subId(arr) {
    let subjectIds = [];
    if (arr && arr.length > 0) {
        arr.map((item) => {
            let ids = item.split('ID:').pop();
            subjectIds.push(ids);
        });
    }
    return subjectIds;
}

export function getIdFromUrl(url) {
    let draftId = url.match(/id=\d+/g);
    if (draftId == null) {
        return null;
    }
    draftId = draftId[0].split("=").pop();
    return draftId;
}

export function arraysEqual(a, b) {
    if (a === b) return true;
    if (a == null || b == null) return false;
    if (a.length != b.length) return false;
    //todo sort
    for (var i = 0; i < a.length; ++i) {
        if (a[i] !== b[i]) return false;
    }
    return true;
}

export function allStocksEquals(a, b) {
    let symbolEqual = a.Symbol == b.Symbol;
    let importanceEqual = a.IsImportant == b.IsImportant;
    let descEqual = a.Desc == b.Desc;
    let DragonHeadEqual = a.DragonHead == b.DragonHead;
    let onDragonTigerBoardEqual = a.OnDragonTigerBoard == b.OnDragonTigerBoard;
    return symbolEqual && importanceEqual && descEqual && DragonHeadEqual && onDragonTigerBoardEqual;
}

export function reachBottom() {
    let h = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
    let s = document.body.scrollTop;
    let total = document.body.scrollHeight;
    return total <= h + s + 150;
}
