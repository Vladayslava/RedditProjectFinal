let page = 1;
let isLoading = false;
let hasMorePosts = true;
let postList;

console.log('Infinite scroll script loaded');

function initInfiniteScroll() {
    console.log('Initializing infinite scroll');
    postList = document.getElementById('post-list');
    if (!postList) {
        console.error('post-list element not found');
        return;
    }
    
    window.addEventListener('scroll', handleScroll);
    console.log('Scroll event listener added');
}

function handleScroll() {
    if (!hasMorePosts || isLoading) {
        return;
    }

    console.log('Scrolling detected');
    console.log('Window inner height:', window.innerHeight);
    console.log('Window scrollY:', window.scrollY);
    console.log('Document body offset height:', document.body.offsetHeight);

    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 100) {
        console.log('Reached bottom of page, loading more posts');
        loadMorePosts();
    }
}

function loadMorePosts() {
    if (!postList || !hasMorePosts || isLoading) {
        return;
    }

    isLoading = true;
    page++;
    console.log('Loading page:', page);

    const sort = new URLSearchParams(window.location.search).get('sort') || 'new';
    const url = `${window.location.pathname}?page=${page}&sort=${sort}`; 
    console.log('Fetching URL:', url);

    document.getElementById('loading-indicator').style.display = 'block';

    fetch(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        console.log('Response status:', response.status);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Received data:', data);
        if (data.html) {
            const newPosts = document.createElement('div');
            newPosts.innerHTML = data.html;
            const postItems = newPosts.querySelector('ul');
            if (postItems && postItems.children.length > 0) {
                Array.from(postItems.children).forEach(item => postList.querySelector('ul').appendChild(item));
            }
        }
        
        hasMorePosts = data.has_next;
        if (!hasMorePosts) {
            console.log('No more posts to load');
            document.getElementById('no-more-posts').style.display = 'block';
        }
    })
    .catch(error => {
        console.error('Error fetching posts:', error);
        hasMorePosts = false;
    })
    .finally(() => {
        isLoading = false;
        document.getElementById('loading-indicator').style.display = 'none';
        console.log('Loading completed');
    });
}

document.addEventListener('DOMContentLoaded', initInfiniteScroll);