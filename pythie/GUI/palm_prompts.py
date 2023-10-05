summary_template = """
Provide a summary with about two sentences for the following {product} review transcript:

{transcript_chunk}

Summary:
"""

video_likes_dislikes_prompt = """
Extract important informations from the following Mazda 2 summary into bullet points:

The Mazda 2 is a compact car that impresses with its sleek design, sporty handling, and efficient performance. With its bold lines and aggressive front grille, the Mazda 2 exudes a sense of dynamism and sophistication. The interior is well-crafted, featuring high-quality materials and modern technology, creating a comfortable and stylish cabin. The car's nimble handling and responsive steering make it a joy to drive, especially in urban environments where its compact size shines. The Mazda 2 also delivers impressive fuel efficiency, making it a practical choice for daily commuting. While it may not offer the most spacious rear seating or cargo capacity in its class, the Mazda 2 compensates with its overall driving enjoyment and attention to detail. Overall, the Mazda 2 is a compelling option for those seeking a small car that combines style, agility, and fuel efficiency.

Mazda 2 likes and dislikes:
Likes:
- Sleek design with bold lines and aggressive front grille
- Sporty handling and nimble maneuverability
- Comfortable and stylish interior with high-quality materials
- Modern technology features
- Impressive fuel efficiency

Dislikes:
- Limited rear seating and cargo capacity compared to some competitors

Extract important informations from the following {product} summary into bullet points:

{combined_chunks_summary}

{product} likes and dislikes:
"""


topics_generation_prompt = """
Provide a list of the general discussed topics about the Mazda 2 based on the following text.
Topics should be one or two words long.
You can generate 6 topics maximum.

Text:
The Mazda 2 is a reliable and efficient vehicle. It offers good fuel economy and has a small, agile design. The car handles well and provides a smooth driving experience. The interior is comfortable and well-designed. It has a user-friendly infotainment system. The Mazda 2 has advanced safety features for its class. The car has a stylish and modern exterior design. It offers good value for its price range. The Mazda 2 has a reputation for being reliable and durable. It has a responsive and efficient engine. The Mazda 2 has limited cargo space, especially compared to larger vehicles. It may feel underpowered on highways or during overtaking. The backseat space is a bit cramped for taller passengers. The infotainment system may lack some advanced features found in competitors. The ride quality can be slightly firm on rough roads. The Mazda 2's standard features may not be as generous as some rivals. It may lack the latest driver-assistance technologies available in higher-end models. The engine noise can be noticeable under heavy acceleration. The Mazda 2 is not available with all-wheel drive. Some customers may find the rear visibility to be limited.

General topics list (6 maximum):
- Design
- Interior
- Safety
- Interior
- Technology
- Performance

Provide a list of the general discussed topics about the {product} based on the following text.
Topics should be one or two words long.
You can generate 6 topics maximum.

Text:
{likes_dislikes_bullet_points}

General topics list (6 maximum):
"""

assign_specific_topics = """
Mazda 2 likes and dislikes:
Likes:
- The Mazda 2 is a reliable and efficient vehicle.
- It offers good fuel economy and has a small, agile design.
- The car handles well and provides a smooth driving experience.
- The interior is comfortable and well-designed.
- It has a user-friendly infotainment system.
- The Mazda 2 has advanced safety features for its class.
- The car has a stylish and modern exterior design.
- It offers good value for its price range.
- The Mazda 2 has a reputation for being reliable and durable.
- It has a responsive and efficient engine.

Dislikes:
- The Mazda 2 has limited cargo space, especially compared to larger vehicles.
- It may feel underpowered on highways or during overtaking.
- The backseat space is a bit cramped for taller passengers.
- The infotainment system may lack some advanced features found in competitors.
- The ride quality can be slightly firm on rough roads.
- The Mazda 2's standard features may not be as generous as some rivals.
- It may lack the latest driver-assistance technologies available in higher-end models.
- The engine noise can be noticeable under heavy acceleration.
- The Mazda 2 is not available with all-wheel drive.
- Some customers may find the rear visibility to be limited.

Assign to each of the Mazda 2 likes and dislikes, one or more topic from the following list: 
- Fuel economy
- Safety
- Infotainment
- Interior
- Price
- Engine
- Drive
- Exterior
- Other

Assigned topics:
Likes:
- The Mazda 2 is a reliable and efficient vehicle. (Other)
- It offers good fuel economy and has a small, agile design. (Fuel economy)
- The car handles well and provides a smooth driving experience. (Drive)
- The interior is comfortable and well-designed. (Interior)
- It has a user-friendly infotainment system. (Infotainment)
- The Mazda 2 has advanced safety features for its class. (Safety)
- The car has a stylish and modern exterior design. (Exterior)
- It offers good value for its price range. (Price)
- The Mazda 2 has a reputation for being reliable and durable. (Other)
- It has a responsive and efficient engine. (Engine, Fuel economy)

Dislikes:
- The Mazda 2 has limited cargo space, especially compared to larger vehicles. (Interior)
- It may feel underpowered on highways or during overtaking. (Engine)
- The backseat space is a bit cramped for taller passengers. (Interior)
- The infotainment system may lack some advanced features found in competitors. (Infotainment)
- The ride quality can be slightly firm on rough roads. (Drive)
- The Mazda 2's standard features may not be as generous as some rivals. (Other)
- It may lack the latest driver-assistance technologies available in higher-end models. (Drive)
- The engine noise can be noticeable under heavy acceleration. (Engine)
- The Mazda 2 is not available with all-wheel drive. (Drive)
- Some customers may find the rear visibility to be limited. (Drive)

{product} likes and dislikes:
{combined_likes_dislikes}

Assign to each of the {product} likes and dislikes, one or more topic from the following list:
{topics_str}

Assigned topics:
"""

condense_points = """
Detect and merge bullet points that represent the same ideas about the HP screen Display. For each new bullet point show the count of the original merged bullet points. Total count assigned in new bullet points should be equal number of original bullet points.
Bullet points:
- Vibrant and accurate colors.
- High resolution.
- The screen features a wide color gamut, allowing for accurate color reproduction.
- Anti-glare coating.
- Resolution that captures intricate details with precision.

New bullet points:
- The screen features a wide color gamut, allowing for vibrant and accurate color reproduction (2)
- High resolution that captures intricate details with precision. (2)
- Anti-glare coating. (1)
Number of original bullet points = 5
Total count assigned in new bullet points = 2 + 2 + 1 = 5

Detect and merge bullet points that represent the same ideas about the Mazda 2 Engine. For each new bullet point show the count of the original merged bullet points. Total count assigned in new bullet points should be equal number of original bullet points.
Bullet points:
- The level of noise produced by the engine can be quite high.
- It may feel underpowered on highways or during overtaking.
- The engine noise can be noticeable under heavy acceleration.
- The engine can be very loud. 

New bullet points:
- The engine can be loud, especially during heavy acceleration. (3)
- It may feel underpowered on highways or during overtaking. (1)
Number of original bullet points = 4
Total count assigned in new bullet points = 3 + 1 = 4

Detect and merge bullet points that represent the same ideas about the {product} {topic}. For each new bullet point show the count of the original merged bullet points. Total count assigned in new bullet points should be equal number of original bullet points.
Bullet points:
{related_points}

New bullet points:
"""

global_summary = """
Provide a summary for the following list of {product} likes and dislikes. Summary should consist of two paragraphs, one for Likes and one for Dislikes, each should be 2 to 3 sentences long.
{local_summary}

Summary:
"""



########### Competitors ###########
chunk_competitors_prompt = """
Answer the user request based on the context below. Answer while providing details. If the user request cannot be answered using the information provided answer with “No competitors informations found”

Context:
{transcript_chunk}

Request: Extract comparison informations between the {product} and other products.
Answer:
"""


competitors_summary_prompt = """
Provide a summary with about three sentences for the context below.
The summary should be focused on the comparison of the {product} to other products.
Transition between summary sentences should be smooth.

Context:
{concat_competitors_info}

Summary focused on competitors comparison:
"""

competitors_products_detection_prompt = """
Given a paragraph comparing the Mazda 2 to other products. Detect the mentioned products in the paragraph. Your response should be in bullet points format.
You can detect 2 products max (if there are more don't include them in your response)
Do not include Mazda 2 in the detected product.

Paragraph:
In comparison to its rivals, the Ford Focus and the Fiat 500, the Mazda 2 stands out with its spirited performance, agile handling, and sporty design. It offers a comfortable and well-designed cabin with ample space for passengers, and its fuel efficiency is impressive with efficient engine options. While the Ford Focus and Fiat 500 have their own unique features, the Mazda 2 strikes a balance between practicality and fun, making it an appealing choice for those seeking an enjoyable driving experience in a compact car.

Detected products (not brands):
- Ford Focus
- Fiat 500

Given a paragraph comparing the {product} to other products. Detect the mentioned products in the paragraph. Your response should be in bullet points format.
You can detect 2 products max (if there are more don't include them in your response)
Do not include {product} in the detected product.

Paragraph:
{concat_competitors_info}

Detected products (not brands):
"""

comparison_prompt = """
Given two paragraphs each describing feature of a product, your task is to compare the two products based on the provided informations.

{main_product} paragraph:
{combined_chunks_summary_main_product}

{product} paragraph:
{combined_chunks_summary_product}

Compare the {main_product} to the {product} based on the provided informations:
"""

########### Topics rating ###########
rate_topics_prompt = """
Mazda 2 likes and dislikes:
Likes:
- The Mazda 2 is a reliable and efficient vehicle. (Other)
- It offers good fuel economy and has a small, agile design. (Fuel economy)
- The car handles well and provides a smooth driving experience. (Drive)
- The interior is comfortable and well-designed. (Interior)
- It has a user-friendly infotainment system. (Infotainment)
- The Mazda 2 has advanced safety features for its class. (Safety)
- The car has a stylish and modern exterior design. (Exterior)
- It offers good value for its price range. (Price)
- The Mazda 2 has a reputation for being reliable and durable. (Other)
- It has a responsive and efficient engine. (Engine)

Dislikes:
- The Mazda 2 has limited cargo space, especially compared to larger vehicles. (Interior)
- It may feel underpowered on highways or during overtaking. (Engine)
- The backseat space is a bit cramped for taller passengers. (Interior)
- The infotainment system may lack some advanced features found in competitors. (Infotainment)
- The ride quality can be slightly firm on rough roads. (Drive)
- The Mazda 2's standard features may not be as generous as some rivals. (Other)
- It may lack the latest driver-assistance technologies available in higher-end models. (Drive)
- The engine noise can be noticeable under heavy acceleration. (Engine)
- The Mazda 2 is not available with all-wheel drive. (Drive)
- Some customers may find the rear visibility to be limited. (Drive)

Based on the above Mazda 2 likes and dislikes, assign a rating between 0 and 10 to each of the following topics:
- Fuel economy
- Safety
- Infotainment
- Interior
- Price
- Engine

Topics rating:
- Fuel economy: 9/10
- Safety: 8/10
- Infotainment: 6/10
- Interior: 6/10
- Price: 8/10
- Engine: 7/10

{product} likes and dislikes:
{assigned_topics_list}

Based on the above {product} likes and dislikes, assign a rating between 0 and 10 to each of the following topics:
{topics_list}

Topics rating:
"""

questions_generation_prompt = """
Replace the "FILL HERE" in the below Incomplete questions by the convenient words to create new questions. For context, use the context below.

Context:
The Mazda 2 is a reliable and efficient vehicle. It offers good fuel economy and has a small, agile design. The car handles well and provides a smooth driving experience. The interior is comfortable and well-designed. It has a user-friendly infotainment system. The Mazda 2 has advanced safety features for its class. The car has a stylish and modern exterior design. It offers good value for its price range. The Mazda 2 has a reputation for being reliable and durable. It has a responsive and efficient engine. The Mazda 2 has limited cargo space, especially compared to larger vehicles. It may feel underpowered on highways or during overtaking. The backseat space is a bit cramped for taller passengers. The infotainment system may lack some advanced features found in competitors. The ride quality can be slightly firm on rough roads. The Mazda 2's standard features may not be as generous as some rivals. It may lack the latest driver-assistance technologies available in higher-end models. The engine noise can be noticeable under heavy acceleration. The Mazda 2 is not available with all-wheel drive. Some customers may find the rear visibility to be limited.

Incomplete questions:
Q1: Generate a SEO blog paragraph, that showcase the FILL HERE of the Mazda 2 FILL HERE.
Q2: Generate 3 ad-copies showcasing the Mazda 2 FILL HERE, with headlines and bodies, and include long-tail keywords on which I can bid on.
Q3: Make an advertising script about the Mazda 2 targeted for FILL HERE.

New questions:
Q1: Generate a SEO blog paragraph, that showcase the technology of the Mazda 2 infotainment system.
Q2: Generate 3 ad-copies showcasing the Mazda 2 safety, with headlines and bodies, and include long-tail keywords on which I can bid on.
Q3: Make an advertising script about the Mazda 2 targeted for budget friendly customers.

Replace the "FILL HERE" in the below Incomplete questions by the convenient words to create new questions. For context, use the context below.

Context:
{global_summary}

Incomplete questions:
Q1: Generate a SEO blog paragraph, that showcase the FILL HERE of the {product} FILL HERE.
Q2: Generate 3 ad-copies showcasing the {product} FILL HERE, with headlines and bodies, and include long-tail keywords on which I can bid on.
Q3: Make an advertising script about the {product} targeted for FILL HERE.

New questions:
"""

repsonse_prompts = """
Given the following extracted parts of a long document and a USER REQUEST, create a final RESPONSE with references ("SOURCES"). 
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
ALWAYS return a "SOURCES" part in your answer.
RESPONSE should be several sentences long.

USER REQUEST: {question}
=========
{summaries}
=========
RESPONSE:
"""