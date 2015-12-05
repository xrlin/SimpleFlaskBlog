function setNavbarHighlight(){
    item = window.location.href.split('/')[4];
    document.querySelector('li > a[id='+item+']').className = 'active';
}

function addLoadEvent(func){
    var oldonload = window.onload;
    if(typeof window.onload != 'function'){
        window.onload=func;
    }
    else {
        window.onload = function(){
                oldonload();
                func();
        }
        }
}

addLoadEvent(setNavbarHighlight);
