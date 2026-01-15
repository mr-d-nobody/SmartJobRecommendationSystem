def extract_skills_from_taxonomy(text, taxonomy):
    text = text.lower()
    found_skills = set()

    for canonical_skill, meta in taxonomy.items():
        for keyword in meta["keywords"]:
            if keyword in text:
                found_skills.add(canonical_skill)
                break

    return list(found_skills)




