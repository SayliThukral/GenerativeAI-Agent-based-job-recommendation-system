document.getElementById("uploadForm").addEventListener("submit", async function(e){

    e.preventDefault();

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

        const matched = data.matched_items || [];
        const mismatched = data.mismatched_items || [];
        const ytData = data.youtube_recommendations || {};

        // Extract videos from the dictionary
        let ytLinksHtml = "";
        for (const category in ytData) {
            const videos = ytData[category];
            videos.forEach(video => {
                ytLinksHtml += `<li><a href="${video.url}" target="_blank">${video.title}</a></li>`;
            });
        }

        let html = `
            <h2>ATS Score: ${data.ats_score || 'N/A'}</h2>

            <h3>Skills You Have</h3>
            <ul>
                ${matched.length > 0 ? matched.map(skill => `<li>${skill}</li>`).join("") : "<li>None found</li>"}
            </ul>

            <h3>Gap Analysis</h3>
            <ul>
                ${mismatched.length > 0 ? mismatched.map(skill => `<li>${skill}</li>`).join("") : "<li>None found</li>"}
            </ul>

            <h3>YouTube Recommendations</h3>
            <ul>
                ${ytLinksHtml !== "" ? ytLinksHtml : "<li>None found</li>"}
            </ul>
        `;

        document.getElementById("result").innerHTML = html;

    } catch (error) {
        console.error("Fetch error:", error);
        document.getElementById("result").innerHTML = `<h3 style="color:red;">Failed to process request. Check browser console.</h3>`;
    }
});