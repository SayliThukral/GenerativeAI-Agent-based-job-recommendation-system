document.getElementById("uploadForm").addEventListener("submit", async function(e){

    e.preventDefault();

    let resume = document.getElementById("resume").files[0];
    let jd = document.getElementById("jd").files[0];

    let formData = new FormData();
    formData.append("resume", resume);
    formData.append("jd", jd);

    let response = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    let data = await response.json();

    if(response.ok){
        alert(data.message);
        console.log(data.result);
    }else{
        alert("Upload failed");
    }

});