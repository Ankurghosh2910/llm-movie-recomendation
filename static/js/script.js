const TMDB_API_KEY = 'YOUR_TMDB_API_KEY'; // You'll need to get this from TMDB
const TMDB_IMAGE_BASE = 'https://image.tmdb.org/t/p/w500';

async function getMoviePoster(title) {
    try {
        console.log('Fetching poster for:', title); // Debug log
        const response = await fetch(`/get_movie_poster?title=${encodeURIComponent(title.trim())}`);
        const data = await response.json();
        console.log('Poster data received:', data); // Debug log
        return data;
    } catch (error) {
        console.error('Error fetching poster:', error);
        return null;
    }
}

async function getRecommendations() {
    const preferences = document.getElementById('preferences').value;
    if (!preferences.trim()) {
        alert('Please enter your movie preferences');
        return;
    }

    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');

    try {
        const formData = new FormData();
        formData.append('preferences', preferences);

        const response = await fetch('/get_recommendations', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        console.log('Recommendations received:', data); // Debug log

        if (data.error) {
            throw new Error(data.error);
        }

        const recommendations = data.recommendations.split('\n').filter(line => line.trim());
        const recommendationsDiv = document.getElementById('recommendations-list');
        recommendationsDiv.innerHTML = '';

        for (const rec of recommendations) {
            const match = rec.match(/(\d+)\.\s+\*\*([^*]+)\*\*\s*-\s*(.+)/);
            if (match) {
                const [_, number, title, description] = match;
                console.log('Processing movie:', title.trim()); // Debug log
                
                const movieData = await getMoviePoster(title.trim());
                console.log('Movie data:', movieData); // Debug log

                const movieCard = document.createElement('div');
                movieCard.className = 'movie-card';

                const posterContent = movieData && movieData.poster ? 
                    `<img src="${movieData.poster}" alt="${title}" class="movie-poster">` :
                    `<div class="movie-poster-placeholder">
                        <div class="movie-icon">🎬</div>
                    </div>`;

                movieCard.innerHTML = `
                    <div class="poster-container">
                        ${posterContent}
                        <div class="poster-overlay">
                            <div class="movie-number">#${number}</div>
                            ${movieData && movieData.year ? 
                                `<div class="movie-year">${movieData.year}</div>` : ''}
                        </div>
                    </div>
                    <div class="movie-info">
                        <div class="movie-title">${title.trim()}</div>
                        <div class="movie-description">${description}</div>
                        <div class="movie-rating">
                            ${movieData && movieData.rating ? 
                                `<span class="imdb-rating">⭐ ${movieData.rating}</span>` : 
                                '<span class="stars">⭐⭐⭐⭐⭐</span>'}
                            <span class="recommend-tag">Recommended</span>
                        </div>
                    </div>
                `;
                recommendationsDiv.appendChild(movieCard);
            }
        }
        
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('results').classList.remove('hidden');

    } catch (error) {
        console.error('Error:', error); // Debug log
        alert('Error getting recommendations: ' + error.message);
        document.getElementById('loading').classList.add('hidden');
    }
}

// Add this to check if the script is loaded
console.log('Movie recommender script loaded'); 