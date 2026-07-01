SKILLS = [
  'python',
  'machine learning',
  'deep learning',
  'sql',
  'mysql',
  'java',
  'power bi',
  'tableau',
  'excel',
  'flask',
  'django',
  'aws',
  'statistics',
  'data analysis',
  'data science',
  'tensorflow',
  'pytorch',
  'c++',
  'html',
  'css',
  'javascript',
  'Keras',
  'Scikit-learn',
  'pandas',
  'numpy',
  'docker',
  'azure',
  'git',
  'github',
  'nlp',
  'computer vision'
]

def extract_skills(text):
    text = text.lower()
    found_skills = []
    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))