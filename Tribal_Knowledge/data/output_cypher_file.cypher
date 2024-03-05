
MERGE (p:Project {name: 'Project_0'})
MERGE (r:Repository {name: 'Project_0_Repo_1'})
ON CREATE SET r.displayName = 'Repo_1'
MERGE (l:Language {name: 'Lua'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 30000000;


MERGE (p:Project {name: 'Project_1'})
MERGE (r:Repository {name: 'Project_1_Repo_1'})
ON CREATE SET r.displayName = 'Repo_1'
MERGE (l:Language {name: 'Java'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 4382078;


MERGE (p:Project {name: 'Project_1'})
MERGE (r:Repository {name: 'Project_1_Repo_1'})
ON CREATE SET r.displayName = 'Repo_1'
MERGE (l:Language {name: 'SQL'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 1233534;


MERGE (p:Project {name: 'Project_1'})
MERGE (r:Repository {name: 'Project_1_Repo_1'})
ON CREATE SET r.displayName = 'Repo_1'
MERGE (l:Language {name: 'Groovy'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 4381;


MERGE (p:Project {name: 'Project_1'})
MERGE (r:Repository {name: 'Project_1_Repo_1'})
ON CREATE SET r.displayName = 'Repo_1'
MERGE (l:Language {name: 'Rust'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 648982;


MERGE (p:Project {name: 'Project_1'})
MERGE (r:Repository {name: 'Project_1_Repo_1'})
ON CREATE SET r.displayName = 'Repo_1'
MERGE (l:Language {name: 'C#'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 1875893;


MERGE (p:Project {name: 'Project_1'})
MERGE (r:Repository {name: 'Project_1_Repo_1'})
ON CREATE SET r.displayName = 'Repo_1'
MERGE (l:Language {name: 'Lua'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 32948;


MERGE (p:Project {name: 'Project_1'})
MERGE (r:Repository {name: 'Project_1_Repo_1'})
ON CREATE SET r.displayName = 'Repo_1'
MERGE (l:Language {name: 'Kotlin'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 1695761;


MERGE (p:Project {name: 'Project_1'})
MERGE (r:Repository {name: 'Project_1_Repo_2'})
ON CREATE SET r.displayName = 'Repo_2'
MERGE (l:Language {name: 'Bash'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 466806;


MERGE (p:Project {name: 'Project_1'})
MERGE (r:Repository {name: 'Project_1_Repo_2'})
ON CREATE SET r.displayName = 'Repo_2'
MERGE (l:Language {name: 'Kotlin'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 727586;


MERGE (p:Project {name: 'Project_1'})
MERGE (r:Repository {name: 'Project_1_Repo_2'})
ON CREATE SET r.displayName = 'Repo_2'
MERGE (l:Language {name: 'Python'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 1906754;


MERGE (p:Project {name: 'Project_1'})
MERGE (r:Repository {name: 'Project_1_Repo_2'})
ON CREATE SET r.displayName = 'Repo_2'
MERGE (l:Language {name: 'Rails'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 67459;


MERGE (p:Project {name: 'Project_1'})
MERGE (r:Repository {name: 'Project_1_Repo_2'})
ON CREATE SET r.displayName = 'Repo_2'
MERGE (l:Language {name: 'Elixir'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 270740;


MERGE (p:Project {name: 'Project_1'})
MERGE (r:Repository {name: 'Project_1_Repo_2'})
ON CREATE SET r.displayName = 'Repo_2'
MERGE (l:Language {name: 'Go'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 459087;


MERGE (p:Project {name: 'Project_1'})
MERGE (r:Repository {name: 'Project_1_Repo_2'})
ON CREATE SET r.displayName = 'Repo_2'
MERGE (l:Language {name: 'JavaScript'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 351838;


MERGE (p:Project {name: 'Project_1'})
MERGE (r:Repository {name: 'Project_1_Repo_2'})
ON CREATE SET r.displayName = 'Repo_2'
MERGE (l:Language {name: 'TypeScript'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 194882;


MERGE (p:Project {name: 'Project_1'})
MERGE (r:Repository {name: 'Project_1_Repo_3'})
ON CREATE SET r.displayName = 'Repo_3'
MERGE (l:Language {name: 'Scala'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 3334020;


MERGE (p:Project {name: 'Project_1'})
MERGE (r:Repository {name: 'Project_1_Repo_3'})
ON CREATE SET r.displayName = 'Repo_3'
MERGE (l:Language {name: 'Rust'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 327428;


MERGE (p:Project {name: 'Project_1'})
MERGE (r:Repository {name: 'Project_1_Repo_4'})
ON CREATE SET r.displayName = 'Repo_4'
MERGE (l:Language {name: 'Python'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 2957610;


MERGE (p:Project {name: 'Project_2'})
MERGE (r:Repository {name: 'Project_2_Repo_1'})
ON CREATE SET r.displayName = 'Repo_1'
MERGE (l:Language {name: 'Python'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 2709092;


MERGE (p:Project {name: 'Project_2'})
MERGE (r:Repository {name: 'Project_2_Repo_2'})
ON CREATE SET r.displayName = 'Repo_2'
MERGE (l:Language {name: 'JavaScript'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 1019474;


MERGE (p:Project {name: 'Project_2'})
MERGE (r:Repository {name: 'Project_2_Repo_2'})
ON CREATE SET r.displayName = 'Repo_2'
MERGE (l:Language {name: 'Swift'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 82515;


MERGE (p:Project {name: 'Project_2'})
MERGE (r:Repository {name: 'Project_2_Repo_2'})
ON CREATE SET r.displayName = 'Repo_2'
MERGE (l:Language {name: 'C#'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 124945;


MERGE (p:Project {name: 'Project_2'})
MERGE (r:Repository {name: 'Project_2_Repo_2'})
ON CREATE SET r.displayName = 'Repo_2'
MERGE (l:Language {name: 'CSS'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 188897;


MERGE (p:Project {name: 'Project_2'})
MERGE (r:Repository {name: 'Project_2_Repo_2'})
ON CREATE SET r.displayName = 'Repo_2'
MERGE (l:Language {name: 'Objective-C'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 172084;


MERGE (p:Project {name: 'Project_2'})
MERGE (r:Repository {name: 'Project_2_Repo_2'})
ON CREATE SET r.displayName = 'Repo_2'
MERGE (l:Language {name: 'Go'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 566432;


MERGE (p:Project {name: 'Project_3'})
MERGE (r:Repository {name: 'Project_3_Repo_1'})
ON CREATE SET r.displayName = 'Repo_1'
MERGE (l:Language {name: 'Python'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 1452553;


MERGE (p:Project {name: 'Project_3'})
MERGE (r:Repository {name: 'Project_3_Repo_1'})
ON CREATE SET r.displayName = 'Repo_1'
MERGE (l:Language {name: 'Julia'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 930289;


MERGE (p:Project {name: 'Project_3'})
MERGE (r:Repository {name: 'Project_3_Repo_2'})
ON CREATE SET r.displayName = 'Repo_2'
MERGE (l:Language {name: 'Bash'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 1124767;


MERGE (p:Project {name: 'Project_3'})
MERGE (r:Repository {name: 'Project_3_Repo_2'})
ON CREATE SET r.displayName = 'Repo_2'
MERGE (l:Language {name: 'Java'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 4760272;


MERGE (p:Project {name: 'Project_3'})
MERGE (r:Repository {name: 'Project_3_Repo_2'})
ON CREATE SET r.displayName = 'Repo_2'
MERGE (l:Language {name: 'Groovy'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 2575454;


MERGE (p:Project {name: 'Project_3'})
MERGE (r:Repository {name: 'Project_3_Repo_2'})
ON CREATE SET r.displayName = 'Repo_2'
MERGE (l:Language {name: 'Clojure'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 468672;


MERGE (p:Project {name: 'Project_3'})
MERGE (r:Repository {name: 'Project_3_Repo_3'})
ON CREATE SET r.displayName = 'Repo_3'
MERGE (l:Language {name: 'HTML'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 1640252;


MERGE (p:Project {name: 'Project_3'})
MERGE (r:Repository {name: 'Project_3_Repo_3'})
ON CREATE SET r.displayName = 'Repo_3'
MERGE (l:Language {name: 'TypeScript'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 1374855;


MERGE (p:Project {name: 'Project_3'})
MERGE (r:Repository {name: 'Project_3_Repo_3'})
ON CREATE SET r.displayName = 'Repo_3'
MERGE (l:Language {name: 'Java'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 3715591;


MERGE (p:Project {name: 'Project_3'})
MERGE (r:Repository {name: 'Project_3_Repo_4'})
ON CREATE SET r.displayName = 'Repo_4'
MERGE (l:Language {name: 'C++'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 646963;


MERGE (p:Project {name: 'Project_3'})
MERGE (r:Repository {name: 'Project_3_Repo_4'})
ON CREATE SET r.displayName = 'Repo_4'
MERGE (l:Language {name: 'C#'})
MERGE (p)-[:CONTAINS]->(r)
MERGE (r)-[uses:USES]->(l)
ON CREATE SET uses.byteCount = 9099830;

