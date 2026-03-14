# Potential Enhancements

## Noodles

- Replace initializer SQL script with persistent DB
    - This solution requires a DB backup solution which can just be accomplished with a cronjob for this environment
- Find solution to download and shrink images down to ~300px wide. We're just using a link right now but some of these images are 2+ MB which won't scale beyond 10 reviews or so without ever-increasing page load times.
- Implement content management system for noodle DB
    - This solution can also help to solve the images issue since the content manager can accept a link which it can use to download and shrink the provided image. Then the data could go into a BLOB column
- Consider creating a dedicated review page for each noodle and linking to the reviews rather than expanding a content section.
    - This would require actual reviews rather than short text. We may simply lack the content for that currently.
- Implement fingernail style filtering for reviews in a style similiar to Spotify "Liked Songs" filtering
    - Filter criteria: price, brand, container type
- Implement review search bar with immediate responsive filtering
- If the review count exceeds 100 or so, we may be forced to implement pagination. This will require an overhaul of the filters mentioned above since they'll need to bounce off the server rather than simply running as a JS filter.
    
## Chess 

- Implement game rules
    - This is probably a huge pain in the ass. Chess rules can vary based on the sanctioning body, but largely in regards to draws and clock rules.
    - Consider the listed example of a player drawing on insufficient material because white ran out their clock in a forced mate position
        - https://www.reddit.com/r/chess/comments/13mh7wm/why_is_this_a_draw_by_timeout_vs_insufficient/
- Replace weird hex tile positioning system with FENs / PGNs
    - This requires more research as well. When I designed the hex placement system, I was unaware that these notation systems existed at all.
- Multiplayer games with server interactivity? This could be done if the rules are hashed out since we have a DB, but it would require the persistent DB listed in the noodles section.