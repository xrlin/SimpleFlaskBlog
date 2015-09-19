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
