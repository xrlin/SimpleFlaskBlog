var dealReplyLink = function(name, reply_to_id){
    document.getElementById('reply_to_id').value = reply_to_id;
    document.getElementById('reply_to_user').value = "" + name;
    //var node=document.createTextNode("reply to " + name);
    var linkNode = document.createElement('a')
    linkNode.setAttribute('id', 'cancel_link')
    linkNode.addEventListener('click', function(event){
        var p = document.getElementById('reply_info')
        document.getElementById('reply_to_id').value = "";
        document.getElementById('reply_to_user').value = "";
        // p.removeChild(document.getElegnmentById('cancel_link'));
        p.innerHTML = "";
    });
    var link_txt = document.createTextNode('取消回复该用户')
    linkNode.appendChild(link_txt)
    //document.getElementById('reply_info').appendChild(node)
    document.getElementById('reply_info').innerHTML = "reply to " + name
    document.getElementById('reply_info').appendChild(linkNode)
}

var markdownPreview = function(){
    document.getElementById('preview').innerHTML =
      marked(document.getElementById('context').value);
}

function setCookie(url, hasViewed, expiretime)
{
var exdate=new Date()
exdate.setTime(exdate.getTime()+expiretime*1000)
//console.log(exdate.toGMTString());
document.cookie=url+ "=" +escape(hasViewed)+
((expiretime==null) ? "" : ";expires="+exdate.toGMTString())
}

function getCookie(c_name)
{
if (document.cookie.length>0)
  {
  c_start=document.cookie.indexOf(c_name + "=")
  if (c_start!=-1)
    { 
    c_start=c_start + c_name.length+1 
    c_end=document.cookie.indexOf(";",c_start)
    if (c_end==-1) c_end=document.cookie.length
    return unescape(document.cookie.substring(c_start,c_end))
    } 
  }
return ""
}

function checkCookie(url){
    hasViewed = getCookie(url)
    console.log(hasViewed)
    return hasViewed
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

function addViewed(){
    url = window.location.href;
    get_url = url + "/addview"
    var xmlHttp = null;
	try{
	xmlHttp = new XMLHttpRequest();
	}catch(e){
	try{
	   xmlHttp=new ActiveXObject("Msxml2.XMLHTTP");
	}catch(e){
	xmlHttp = new ActiveXObject("Microsoft.XMLHttp");	}
	}
    if (!checkCookie(url)) {
	
	xmlHttp.open("GET", get_url, true)
	xmlHttp.send()
	console.log(xmlHttp.responseText) 
	setCookie(url, true, 3600)
	}
    }
	
function setNavbarHighlight(){
    item = window.location.href.split('/')[4];
    document.querySelector('li[id='+item+']').className = 'active';
}

addLoadEvent(addViewed);	
//addLoadEvent(setNavbarHighlight)
   
