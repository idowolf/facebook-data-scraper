import requests

access_token = 'ACCESS_TOKEN_HERE'
url = 'https://graph.facebook.com/v13.0/me/posts'
your_username = 'YOUR_FACEBOOK_USERNAME'
params = {
    'fields': 'id,message,attachments{media,type,url},permalink_url',
    'limit': '100',
    'access_token': access_token
}

def fetch_posts(url, params):
    posts = []
    while True:
        response = requests.get(url, params=params).json()
        for post in response['data']:
            post_id = post['id']
            post_message = post.get('message', 'No message content')
            post_link = post.get('permalink_url', '')
            embed_code = ''
            if 'attachments' in post:
                for attachment in post['attachments']['data']:
                    if attachment['type'] == 'video':
                        video_url = attachment['media']['source']
                        if "youtube" in video_url:
                            embed_code += f'<iframe width="560" height="315" src="{video_url}" frameborder="0" allowfullscreen></iframe>'
                    elif attachment['type'] == 'photo':
                        photo_url = attachment['media']['image']['src']
                        embed_code += f'<img src="{photo_url}" alt="Facebook photo" style="max-width:100%;">'
            posts.append((post_id, post_link, post_message, embed_code))
        if 'paging' in response and 'next' in response['paging']:
            params = None
            url = response['paging']['next']
        else:
            break
    return posts

text_posts = fetch_posts(url, params)

# Writing HTML output to a file
with open('out.html', 'w', encoding='utf-8') as file:
    file.write('<html><head><title>Facebook Posts</title></head><body>')
    file.write('<table border="1"><tr><th>Link to Post</th><th>Other Link</th><th>Post Content</th></tr>')
    for post_id, post_link, post_message, embed_code in text_posts:
        # Assuming post_id is number_number, take the second number
        trimmed_post_id = post_id.split('_')[1]
        delete_link = f'https://www.facebook.com/{post_id}/delete'  # Hypothetical delete link, adjust as needed
        file.write(f'<tr><td><a href="{post_link}" target="_blank">View Post</a></td>')
        file.write(f'<td><a href="https://www.facebook.com/{your_username}/posts/{trimmed_post_id}" target="_blank">Other Link</a></td>')
        file.write(f'<td>{post_message}<br>{embed_code}</td>')
    file.write('</table></body></html>')

print("HTML file generated successfully.")
