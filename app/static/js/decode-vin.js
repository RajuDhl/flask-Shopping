function decodeVin(vin) {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let response = JSON.parse(xhr.responseText);
            let d = response.Results[0];
            document.getElementById("vin-decode").innerHTML = d["ModelYear"]+" "+d["Make"]+" "+d["Model"]+" "+d["Trim"];
            document.getElementById('year').value = d["ModelYear"];
            document.getElementById('make').value = d["Make"];
            document.getElementById('model').value = d["Model"];
            document.getElementById('trim').value = d["Trim"];
        }
    }
    if (!document.getElementById('year').value) {
        let url = 'https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/';
        url += vin + '?format=json';
        xhr.open("GET", url, true);
        xhr.send();
    }
}

function postForm(post_to_pathname) {
    console.log("the post form hit ")
   const xhr = new XMLHttpRequest();
   xhr.onreadystatechange = function() {
   if (xhr.readyState === XMLHttpRequest.DONE) {
       if (xhr.status === 200) {
           location.replace(window.location.pathname = '/repo-log?msg='
               + JSON.parse(xhr.responseText)['msg']);
       }
       else {
           console.log ('Error: ' + xhr.status);
       }
   }
   };
   const data = {};
   //const myTable = document.getElementById("data");
   const matches = document.querySelectorAll("input");
   matches.forEach(function(match) {
       data[match.name] = match.value;
       if (match.type === 'date'){
           data[match.name] = new Date(match.value);
       }
   });

   data['notes'] = document.getElementById('notes').value;
   data['status'] = document.getElementById('status').value;
   // data['reason'] = document.getElementById('reason').value;
   data['reason'] = "";
   data['repo_category']=document.getElementById('repo_category').value;

   var brands = $('#repo_category option:selected');
   var selected = [];
   $(brands).each(function(index, brand){
       selected.push($(this).val());
   });
   data['repo_category'] = selected
   console.log(selected);
   delete data[""]
  //console.log("repo_category=====>",document.getElementById("repo_category").value)
  console.log('data: ' + JSON.stringify(data));

   xhr.open('POST', post_to_pathname, true);
   xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
   xhr.send(JSON.stringify(data));



}
function postExtensionForm(post_to_pathname) {
   const xhr = new XMLHttpRequest();
   xhr.onreadystatechange = function() {
   if (xhr.readyState === XMLHttpRequest.DONE) {
       if (xhr.status === 200) {
           location.replace(window.location.pathname = '/extension-log?msg=' + JSON.parse(xhr.responseText)['msg']);

       }
       else {
           console.log ('Error: ' + xhr.status);
       }
   }
   };
   const data = {};
   //const myTable = document.getElementById("data");
   const matches = document.querySelectorAll("input");
   matches.forEach(function(match) {
       data[match.name] = match.value;
       if (match.type === 'date'){
           data[match.name] = new Date(match.value);
       }
   });
   data['final_status'] = document.getElementById('final_status').value;
   data['approved_by'] = document.getElementById('approved_by').value;
   data['extension_type'] = document.getElementById('extension_type').value;
   data['collector'] = document.getElementById('collector').value;
   console.log(JSON.stringify(data))
   xhr.open('POST', post_to_pathname, true);
   xhr.setRequestHeader('Content-Type', 'application/json');
   xhr.send(JSON.stringify(data));

}
function postPifForm(post_to_pathname) {
   const xhr = new XMLHttpRequest();
   xhr.onreadystatechange = function() {
   if (xhr.readyState === XMLHttpRequest.DONE) {
       if (xhr.status === 200) {
           location.replace(window.location.pathname = '/pif-log?msg=' + JSON.parse(xhr.responseText)['msg']);
       }
       else {
           console.log ('Error: ' + xhr.status);
       }
   }
   };
   const data = {};
   //const myTable = document.getElementById("data");
   const matches = document.querySelectorAll("input");
   matches.forEach(function(match) {
       data[match.name] = match.value;
       if (match.type === 'date'){
           data[match.name] = new Date(match.value);
       }
   });
   data['status'] = document.getElementById('status').value;
   data['comments'] = document.getElementById('comments').value;
   console.log("post", post_to_pathname, JSON.stringify(data))
   xhr.open('POST', post_to_pathname, true);
   xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
   xhr.send(JSON.stringify(data));

}

function postFollowUpForm(post_to_pathname) {
   const xhr = new XMLHttpRequest();
   xhr.onreadystatechange = function() {
   if (xhr.readyState === XMLHttpRequest.DONE) {
       if (xhr.status === 200) {
           console.log("Success")
           location.replace(window.location.pathname = '/title-follow-up?msg=' + JSON.parse(xhr.responseText)['msg']);
       }
       else {
           console.log("failed")
           console.log ('Error: ' + xhr.status);
       }
   }
   };
   const data = {};
   //const myTable = document.getElementById("data");
   const matches = document.querySelectorAll("input[name]");
   matches.forEach(function(match) {
       data[match.name] = match.value;
       if (match.type === 'date'){
           data[match.name] = new Date(match.value);
       }
   });
    data['follow_up_comments'] = document.getElementById('comments').value;
   console.log("post to pathname", post_to_pathname)
    console.log("post", post_to_pathname, JSON.stringify(data))
    xhr.open('POST', post_to_pathname, true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.send(JSON.stringify(data));
}