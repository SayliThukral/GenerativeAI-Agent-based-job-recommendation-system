// ✅ Function to extract YouTube video ID
function getVideoId(url) {
    const regExp = /(?:youtube\.com.*v=|youtu\.be\/)([^&]+)/;
    const match = url.match(regExp);
    return match ? match[1] : "";
}

document.getElementById("uploadForm").addEventListener("submit", async function(e){

    e.preventDefault();

    // ✅ SHOW LOADING
    document.getElementById("loading").style.display = "block";

    // ✅ Clear old result
    document.getElementById("result").innerHTML = "";

    // ✅ Disable button
    document.querySelector("button").disabled = true;

    const formData = new FormData();
    formData.append("resume", document.getElementById("resume").files[0]);
    formData.append("jd", document.getElementById("jd").files[0]);

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            document.getElementById("result").innerHTML = `<h3 style="color:red;">Error: ${data.error}</h3>`;
            return;
        }

        const mismatched = data.mismatched_items || [];
        const ytData = data.youtube_recommendations || {};
        
        

        // ✅ NEW: Thumbnail UI
        let ytLinksHtml = `<div style="display:flex; flex-wrap:wrap; gap:20px;">`;
        let hasVideos = false; // ✅ FIX: Added check so "None found" works correctly

        for (const category in ytData) {
            const videos = ytData[category];
            
            if (videos && videos.length > 0) {
                hasVideos = true;
                videos.forEach(video => {
                    const videoId = getVideoId(video.url);

                    ytLinksHtml += `
                        <div style="width:300px; border-radius:10px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.1);">
                            <a href="${video.url}" target="_blank" style="text-decoration:none; color:black;">
                                <img src="https://img.youtube.com/vi/${videoId}/0.jpg" 
                                     style="width:100%; height:auto;">
                                <div style="padding:10px;">
                                    <p style="font-size:14px;">${video.title}</p>
                                </div>
                            </a>
                        </div>
                    `;
                });
            }
        }

        ytLinksHtml += `</div>`;

        
        let html = `
            <h2>ATS Score: ${data.ats_score || 'N/A'}</h2>

            
            <h3>Gap Analysis</h3>
            <ul>
                ${mismatched.length > 0 ? mismatched.map(skill => `<li>${skill}</li>`).join("") : "<li>None found</li>"}
            </ul>

            <h3>YouTube Recommendations</h3>
            ${hasVideos ? ytLinksHtml : "<p>None found</p>"}
        `;

        document.getElementById("result").innerHTML = html;

    } catch (error) {
        console.error("Fetch error:", error);
        document.getElementById("result").innerHTML = `<h3 style="color:red;">Failed to process request.</h3>`;
    } finally {
        // ✅ HIDE LOADING
        document.getElementById("loading").style.display = "none";
        document.querySelector("button").disabled = false;
    }
});