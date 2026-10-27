"""Regenerates app/data/*.json. Edit the dicts below, run `python make_data.py`."""
import json
S = lambda name, cat, *al: {"name": name, "category": cat, "aliases": list(al)}
SKILLS = {
 "python": S("Python","Programming","py","python3"),
 "java": S("Java","Programming"),
 "c++": S("C++","Programming","cpp","c plus plus"),
 "javascript": S("JavaScript","Programming","js","ecmascript","es6"),
 "typescript": S("TypeScript","Programming","ts"),
 "data structures": S("Data Structures & Algorithms","CS Core","dsa","algorithms","data structures and algorithms"),
 "oop": S("OOP","CS Core","object oriented programming","object-oriented programming","object oriented design"),
 "system design": S("System Design","CS Core","software architecture","scalable systems"),
 "sql": S("SQL","Data","mysql","postgresql","postgres","sqlite","t-sql","pl/sql"),
 "excel": S("Excel","Data","ms excel","microsoft excel","spreadsheets","advanced excel"),
 "power bi": S("Power BI","Data","powerbi","power-bi"),
 "tableau": S("Tableau","Data"),
 "pandas": S("Pandas","Data"),
 "numpy": S("NumPy","Data"),
 "statistics": S("Statistics","Data","statistical analysis","hypothesis testing","probability"),
 "data visualization": S("Data Visualization","Data","data visualisation","dashboards","dashboard development","data viz"),
 "data cleaning": S("Data Cleaning","Data","data wrangling","data preprocessing","data preparation"),
 "etl": S("ETL","Data","data pipelines","data pipeline","elt"),
 "mongodb": S("MongoDB","Data","nosql"),
 "machine learning": S("Machine Learning","AI/ML","ml","predictive modeling","predictive modelling"),
 "deep learning": S("Deep Learning","AI/ML","neural networks","cnn","rnn"),
 "scikit-learn": S("Scikit-learn","AI/ML","sklearn","scikit learn"),
 "tensorflow": S("TensorFlow","AI/ML","keras"),
 "pytorch": S("PyTorch","AI/ML"),
 "nlp": S("NLP","AI/ML","natural language processing"),
 "html": S("HTML","Web","html5"),
 "css": S("CSS","Web","css3","tailwind","tailwind css","sass"),
 "react": S("React","Web","react.js","reactjs","react js"),
 "node.js": S("Node.js","Web","nodejs","node js","express","express.js"),
 "rest api": S("REST APIs","Web","restful api","restful apis","rest apis","api development","apis","web services"),
 "fastapi": S("FastAPI","Web"),
 "django": S("Django","Web"),
 "flask": S("Flask","Web"),
 "aws": S("AWS","Cloud & DevOps","amazon web services","ec2","s3"),
 "azure": S("Azure","Cloud & DevOps","microsoft azure"),
 "gcp": S("GCP","Cloud & DevOps","google cloud","google cloud platform"),
 "docker": S("Docker","Cloud & DevOps","containers","containerization","containerisation"),
 "kubernetes": S("Kubernetes","Cloud & DevOps","k8s"),
 "linux": S("Linux","Cloud & DevOps","unix","ubuntu"),
 "ci/cd": S("CI/CD","Cloud & DevOps","cicd","continuous integration","continuous delivery","github actions","jenkins"),
 "git": S("Git","Cloud & DevOps","github","version control","gitlab"),
 "terraform": S("Terraform","Cloud & DevOps","infrastructure as code","iac"),
 "networking": S("Networking","Cloud & DevOps","tcp/ip","computer networks","dns"),
 "shell scripting": S("Shell Scripting","Cloud & DevOps","bash","bash scripting"),
 "figma": S("Figma","Design","adobe xd","sketch"),
 "wireframing": S("Wireframing & Prototyping","Design","wireframes","prototyping","prototypes"),
 "user research": S("User Research","Design","ux research","user interviews","user testing"),
 "usability testing": S("Usability Testing","Design","usability studies","a/b testing"),
 "ui design": S("UI Design","Design","visual design","interface design","ui/ux design"),
 "design systems": S("Design Systems","Design","component libraries","style guides"),
 "communication": S("Communication","Professional","communication skills","stakeholder management","presentation skills","storytelling"),
}
C = lambda id, title, desc, tags, sal, **sk: {"id": id, "title": title, "description": desc, "tags": tags, "salary_lpa": sal, "skills": {k.replace("_"," ").replace("cicd","ci/cd").replace("nodejs","node.js").replace("restapi","rest api").replace("scikit learn","scikit-learn"): v for k, v in sk.items()}}
CAREERS = [
 C("backend","Backend Developer","Builds APIs, databases and server logic.",["backend","software"],[4,10],python=2,java=2,sql=3,restapi=3,git=2,data_structures=3,oop=2,docker=2,django=1,fastapi=1,linux=1,system_design=1,**{"c++":1}),
 C("frontend","Frontend Developer","Builds responsive, interactive web interfaces.",["frontend","web","software"],[3.5,9],html=3,css=3,javascript=3,react=3,typescript=2,git=2,restapi=2,figma=1,ui_design=1),
 C("fullstack","Full-Stack Developer","Owns both the interface and the server side of web apps.",["web","backend","frontend","software"],[4,10],javascript=3,react=3,nodejs=3,sql=2,restapi=3,html=2,css=2,git=2,mongodb=1,docker=1,typescript=1),
 C("data-analyst","Data Analyst","Turns raw data into insight with queries and dashboards.",["data","analytics"],[3.5,8],sql=3,excel=3,python=2,power_bi=2,tableau=2,data_visualization=3,statistics=2,pandas=2,data_cleaning=2,communication=1),
 C("bi-developer","SQL / BI Developer","Designs data models, ETL jobs and reporting layers.",["data","analytics"],[4,9],sql=3,power_bi=3,etl=3,excel=2,data_visualization=2,tableau=1,data_cleaning=2,python=1,communication=1),
 C("ml-engineer","Machine Learning Engineer","Builds and ships predictive models.",["ai","data"],[5,14],python=3,machine_learning=3,statistics=3,numpy=2,pandas=2,scikit_learn=3,deep_learning=2,tensorflow=2,pytorch=2,sql=1,git=1,nlp=1,docker=1),
 C("cloud","Cloud Engineer","Designs and operates cloud infrastructure.",["cloud","devops"],[4.5,11],aws=3,linux=3,networking=2,docker=2,kubernetes=2,terraform=1,cicd=2,python=1,git=2,azure=1,gcp=1),
 C("devops","DevOps Engineer","Automates build, deploy and monitoring pipelines.",["devops","cloud"],[4.5,11],linux=3,docker=3,cicd=3,kubernetes=2,git=3,aws=2,terraform=2,python=1,networking=1,shell_scripting=2),
 C("uiux","UI/UX Designer","Researches users and designs usable interfaces.",["design"],[3,9],figma=3,wireframing=3,user_research=3,ui_design=3,usability_testing=2,design_systems=1,html=1,css=1,communication=2),
]
for c in CAREERS:
    c["skills"] = {("c++" if k=="c  " else k): v for k, v in c["skills"].items()}
    for k in c["skills"]: assert k in SKILLS, (c["id"], k)
json.dump(SKILLS, open("app/data/skills.json","w"), indent=1)
json.dump({"_note":"Seed data: salary ranges are illustrative entry-level INR LPA estimates. Replace with figures from real postings.","careers":CAREERS}, open("app/data/careers.json","w"), indent=1)
print(len(SKILLS), "skills,", len(CAREERS), "careers")
