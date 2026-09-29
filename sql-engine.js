/* ===== M6 Practice Arena — shared SQL engine, editor, and grading logic =====
   Loads sql.js (real SQLite compiled to WASM) from cdnjs, seeds an in-memory
   University DB + Banking DB, and exposes helpers each m6_practice_*.html
   page uses to render its 15 practice cards (5 basic / 5 intermediate / 5 advanced). */

var SQL_ENGINE = (function () {
  var SQLlib = null;
  var pristineBytes = null;
  var readyPromise = null;

  var SEED_SQL = [
    "CREATE TABLE department (dept_name TEXT PRIMARY KEY, building TEXT, budget NUMERIC);",
    "CREATE TABLE instructor (instructor_id INTEGER PRIMARY KEY, name TEXT, dept_name TEXT REFERENCES department(dept_name), salary NUMERIC);",
    "CREATE TABLE student (student_id INTEGER PRIMARY KEY, name TEXT, dept_name TEXT REFERENCES department(dept_name), tot_cred INTEGER);",
    "CREATE TABLE course (course_id TEXT PRIMARY KEY, title TEXT, dept_name TEXT REFERENCES department(dept_name), credits INTEGER);",
    "CREATE TABLE section (course_id TEXT REFERENCES course(course_id), section_id INTEGER, semester TEXT, year INTEGER, building TEXT, room_number TEXT, PRIMARY KEY (course_id, section_id, semester, year));",
    "CREATE TABLE takes (student_id INTEGER REFERENCES student(student_id), course_id TEXT, section_id INTEGER, semester TEXT, year INTEGER, grade TEXT, PRIMARY KEY (student_id, course_id, section_id, semester, year));",
    "CREATE TABLE teaches (instructor_id INTEGER REFERENCES instructor(instructor_id), course_id TEXT, section_id INTEGER, semester TEXT, year INTEGER, PRIMARY KEY (instructor_id, course_id, section_id, semester, year));",
    "CREATE TABLE advisor (student_id INTEGER REFERENCES student(student_id), instructor_id INTEGER REFERENCES instructor(instructor_id), PRIMARY KEY (student_id));",
    "CREATE TABLE prereq (course_id TEXT REFERENCES course(course_id), prereq_id TEXT REFERENCES course(course_id), PRIMARY KEY (course_id, prereq_id));",

    "INSERT INTO department VALUES ('Comp. Sci.','Taylor',100000),('Physics','Watson',70000),('Math','Chandler',80000),('History','Painter',50000),('Biology','Watson',90000),('Elec. Eng.','Taylor',85000),('Finance','Painter',120000),('Accounting','Painter',95000);",
    "INSERT INTO instructor VALUES (10101,'Brandt','Comp. Sci.',98000),(10102,'Katz','Comp. Sci.',75000),(15151,'Bourikas','Comp. Sci.',90000),(22222,'Kim','Elec. Eng.',80000),(33333,'Srinivasan','Finance',65000),(45565,'Chen','Physics',94000),(58583,'Wu','Math',90000),(76543,'Singh','Biology',80000);",
    "INSERT INTO student VALUES (101,'Zhang','Comp. Sci.',102),(102,'Shankar','Comp. Sci.',102),(128,'Levy','Physics',46),(133,'Brown','Comp. Sci.',58),(139,'Aoi','Elec. Eng.',60),(141,'Chavez','Finance',110),(145,'Okada','Math',34),(148,'Wright','History',22),(150,'Nakamura','Biology',15),(155,'Silva','Comp. Sci.',96),(160,'Patel','Elec. Eng.',88),(165,'Kobayashi','Finance',12),(170,'Garcia','Math',72),(175,'Suzuki','History',95),(180,'Novak','Biology',54),(185,'Lindgren','Comp. Sci.',28),(190,'Petrov','Physics',66),(195,'Costa','Accounting',101),(200,'Ueda','Accounting',40),(205,'Volkov','Music',20);",
    "INSERT INTO course VALUES ('CS-101','Intro. to Computer Science','Comp. Sci.',4),('CS-190','Game Design','Comp. Sci.',4),('CS-315','Robotics','Comp. Sci.',3),('CS-347','Database System Concepts','Comp. Sci.',3),('EE-181','Intro. to Digital Systems','Elec. Eng.',3),('PHY-101','Physics I','Physics',4),('MAT-201','Calculus II','Math',4),('HIS-351','World History','History',3),('BIO-101','Intro. to Biology','Biology',4),('FIN-201','Corporate Finance','Finance',3),('ACC-101','Financial Accounting','Accounting',3);",
    "INSERT INTO prereq VALUES ('CS-190','CS-101'),('CS-315','CS-101'),('CS-347','CS-101'),('EE-181','PHY-101');",
    "INSERT INTO section VALUES ('CS-101',1,'Fall',2023,'Taylor','101'),('CS-101',1,'Spring',2024,'Taylor','101'),('CS-190',1,'Spring',2024,'Taylor','102'),('CS-315',1,'Fall',2023,'Taylor','103'),('CS-347',1,'Fall',2023,'Taylor','104'),('CS-347',1,'Spring',2024,'Taylor','104'),('EE-181',1,'Fall',2023,'Taylor','201'),('PHY-101',1,'Fall',2023,'Watson','100'),('MAT-201',1,'Spring',2024,'Chandler','50'),('HIS-351',1,'Fall',2023,'Painter','20'),('BIO-101',1,'Spring',2024,'Watson','10'),('FIN-201',1,'Fall',2023,'Painter','30'),('ACC-101',1,'Spring',2024,'Painter','31');",
    "INSERT INTO teaches VALUES (10101,'CS-101',1,'Fall',2023),(10101,'CS-347',1,'Fall',2023),(10102,'CS-101',1,'Spring',2024),(15151,'CS-315',1,'Fall',2023),(15151,'CS-190',1,'Spring',2024),(15151,'CS-347',1,'Spring',2024),(22222,'EE-181',1,'Fall',2023),(45565,'PHY-101',1,'Fall',2023),(58583,'MAT-201',1,'Spring',2024),(76543,'BIO-101',1,'Spring',2024),(33333,'FIN-201',1,'Fall',2023);",
    "INSERT INTO advisor VALUES (101,10101),(102,10101),(133,10101),(141,10102),(139,33333),(145,33333);",
    "INSERT INTO takes VALUES (101,'CS-101',1,'Fall',2023,'A'),(101,'CS-347',1,'Fall',2023,'A-'),(102,'CS-101',1,'Fall',2023,'B+'),(102,'CS-315',1,'Fall',2023,'A'),(133,'CS-101',1,'Fall',2023,'B'),(133,'CS-190',1,'Spring',2024,'A'),(155,'CS-101',1,'Spring',2024,'A'),(155,'CS-347',1,'Spring',2024,'B+'),(185,'CS-101',1,'Spring',2024,'C'),(139,'EE-181',1,'Fall',2023,'A-'),(160,'EE-181',1,'Fall',2023,'B'),(190,'PHY-101',1,'Fall',2023,'A'),(145,'MAT-201',1,'Spring',2024,'B'),(170,'MAT-201',1,'Spring',2024,'A-'),(148,'HIS-351',1,'Fall',2023,'A'),(175,'HIS-351',1,'Fall',2023,'B+'),(150,'BIO-101',1,'Spring',2024,'B'),(180,'BIO-101',1,'Spring',2024,'A'),(141,'FIN-201',1,'Fall',2023,'A'),(165,'FIN-201',1,'Fall',2023,'C+'),(195,'ACC-101',1,'Spring',2024,'A'),(200,'ACC-101',1,'Spring',2024,'B');",

    "CREATE TABLE branch (branch_name TEXT PRIMARY KEY, branch_city TEXT, assets NUMERIC);",
    "CREATE TABLE customer (customer_id TEXT PRIMARY KEY, customer_name TEXT, customer_street TEXT, customer_city TEXT);",
    "CREATE TABLE account (account_number TEXT PRIMARY KEY, branch_name TEXT REFERENCES branch(branch_name), balance NUMERIC);",
    "CREATE TABLE depositor (customer_id TEXT REFERENCES customer(customer_id), account_number TEXT REFERENCES account(account_number), PRIMARY KEY (customer_id, account_number));",
    "CREATE TABLE loan (loan_number TEXT PRIMARY KEY, branch_name TEXT REFERENCES branch(branch_name), amount NUMERIC);",
    "CREATE TABLE borrower (customer_id TEXT REFERENCES customer(customer_id), loan_number TEXT REFERENCES loan(loan_number), PRIMARY KEY (customer_id, loan_number));",

    "INSERT INTO branch VALUES ('Brooklyn Bank','Brooklyn',9000000),('Brooklyn Bridge Bank','Brooklyn',3700000),('Midtown Bank','Manhattan',5000000),('Downtown Bank','Manhattan',4200000),('Bronx Central Bank','Bronx',2100000);",
    "INSERT INTO customer VALUES ('10001','Alex Johnson','Grand Concourse','Bronx'),('10002','Hank Irwin','River Ave','Bronx'),('10003','Maria Chen','Grand Concourse','Bronx'),('10004','Sara Johnson','Ocean Pkwy','Brooklyn'),('10005','Wei Tanaka','Flatbush Ave','Brooklyn'),('10006','Omar Diaz','5th Ave','Manhattan'),('10007','Priya Nair','Broadway','Manhattan'),('10008','Liam Byrne','Grand Concourse','Bronx');",
    "INSERT INTO account VALUES ('A-101','Brooklyn Bank',42000),('A-102','Brooklyn Bank',38656),('A-103','Brooklyn Bridge Bank',51000),('A-104','Midtown Bank',15000),('A-105','Midtown Bank',27000),('A-106','Downtown Bank',9000),('A-107','Bronx Central Bank',12000),('A-108','Brooklyn Bank',60000);",
    "INSERT INTO depositor VALUES ('10001','A-101'),('10002','A-102'),('10003','A-103'),('10004','A-108'),('10005','A-104'),('10006','A-105'),('10007','A-106'),('10008','A-107');",
    "INSERT INTO loan VALUES ('L-201','Brooklyn Bank',15000),('L-202','Brooklyn Bridge Bank',9000),('L-203','Midtown Bank',22000),('L-204','Downtown Bank',5000);",
    "INSERT INTO borrower VALUES ('10002','L-201'),('10002','L-202'),('10003','L-201'),('10006','L-203');",

    /* M7: job-postings table used by the data-wrangling practice pages */
    "CREATE TABLE ds_jobs (post_id INTEGER PRIMARY KEY, job_title TEXT, salary_estimate TEXT, job_description TEXT, rating REAL, company_name TEXT, location TEXT, headquarters TEXT, size TEXT, founded INTEGER, type_of_ownership TEXT, industry TEXT, sector TEXT, revenue TEXT, competitors TEXT);",
    "INSERT INTO ds_jobs (post_id, job_title, salary_estimate, job_description, rating, company_name, location, headquarters, size, founded, type_of_ownership, industry, sector, revenue, competitors) VALUES (1,'Data Scientist','$110K-$163K (Glassdoor est.)','Build recommendation models for streaming content.',4.4,'Bluepeak Studios4.4','Burbank, CA','Burbank, CA','10000+ employees',1923,'Company - Public','Motion Picture Production','Media','$10+ billion (USD)','Starlight Media, Orbit Films'),(2,'Senior Data Scientist','$137K-$171K (Glassdoor est.)','Lead analytics projects for federal clients.',3.9,'Ironwood Consulting3.9','McLean, VA','McLean, VA','10000+ employees',1914,'Company - Private','Consulting','Business Services','$10+ billion (USD)','Vantage Group, Kessler & Co'),(3,'Data Analyst','$45K-$79K (Glassdoor est.)','Analyze clinical trial and sales data.',3.6,'Novaline Pharma3.6','Cambridge, MA','Osaka, Japan','10000+ employees',1781,'Company - Public','Biotech & Pharmaceuticals','Biotech & Pharma','$10+ billion (USD)','Curewell, Medisphere'),(4,'Data Scientist','$91K-$150K (Glassdoor est.)','Support outcomes research for cancer patients.',-1,'Open Door Health','Orange, CA','Orange, CA','51 to 200 employees',1998,'Nonprofit Organization','Health Care Services & Hospitals','Health Care','Unknown / Non-Applicable','-1'),(5,'Sr. Data Scientist','$101K-$165K (Glassdoor est.)','Develop machine learning tools for energy research.',4.1,'Pacific Grid Laboratory4.1','Richland, WA','Richland, WA','1001 to 5000 employees',1965,'Government','Federal Agencies','Government','$1 to $2 billion (USD)','-1'),(6,'Data Engineer','$79K-$131K (Glassdoor est.)','Design and maintain ETL pipelines.',4.2,'District 94.2','Dallas, TX','Dallas, TX','201 to 500 employees',2005,'Company - Private','IT Services','Information Technology','$50 to $100 million (USD)','-1'),(7,'Machine Learning Engineer','$124K-$198K (Glassdoor est.)','Train models on genetic and survey data.',3.8,'23Genomics3.8','Sunnyvale, CA','Sunnyvale, CA','501 to 1000 employees',2006,'Company - Private','Biotech & Pharmaceuticals','Biotech & Pharma','$100 to $500 million (USD)','HelixTrace, GeneNest'),(8,'Data Analyst','$52K-$87K (Employer est.)','Report on vehicle quality and warranty data.',3.5,'Kestrel Motor Works3.5','Dearborn, MI','Dearborn, MI','10000+ employees',1903,'Company - Public','Transportation Equipment Manufacturing','Manufacturing','$10+ billion (USD)','Falcon Auto, Ridgeline Motors'),(9,'Sr Data Scientist','$98K-$154K (Glassdoor est.)','Personalize playlists and podcast recommendations.',3.8,'Streamline Audio3.8','New York, NY','Stockholm, Sweden','5001 to 10000 employees',2006,'Company - Private','Internet','Information Technology','$1 to $2 billion (USD)','Tunehive, Echo Labs, SoundArc'),(10,'Business Intelligence Analyst','$61K-$96K (Glassdoor est.)','Build dashboards for supply chain performance.',3.3,'Meridian Food Supply3.3','Houston, TX','Houston, TX','10000+ employees',1969,'Company - Public','Wholesale','Business Services','$10+ billion (USD)','-1'),(11,'Data Scientist','$75K-$133K (Glassdoor est.)','TBD',-1,'Brightside Labs','Austin, TX','-1','1 to 50 employees',-1,'Unknown','-1','-1','Unknown / Non-Applicable','-1'),(12,'Senior Data Scientist','$140K-$190K (Glassdoor est.)','Optimize content delivery and personalization.',4.6,'Cascade Streaming4.6','Los Gatos, CA','Los Gatos, CA','5001 to 10000 employees',1997,'Company - Public','Internet','Information Technology','$10+ billion (USD)','Bluepeak Studios, Orbit Films'),(13,'Data Engineer','$88K-$142K (Glassdoor est.)','Build streaming data platforms on the cloud.',3.9,'Summit Financial3.9','McLean, VA','McLean, VA','10000+ employees',1994,'Company - Public','Banks & Credit Unions','Finance','$10+ billion (USD)','Anchor Bank, Crestline Credit'),(14,'Machine Learning Engineer','$115K-$176K (Glassdoor est.)','Improve perception models for driver assistance.',4.0,'Voltaic Motors4.0','Palo Alto, CA','Austin, TX','10000+ employees',2003,'Company - Private','Transportation Equipment Manufacturing','Manufacturing','$10+ billion (USD)','-1'),(15,'Senior. Data Scientist -','$108K-$160K (Glassdoor est.)','Apply statistics to patient outcomes.',3.7,'Lakeview Medical Center3.7','Rochester, MN','Rochester, MN','10000+ employees',1864,'Nonprofit Organization','Health Care Services & Hospitals','Health Care','$10+ billion (USD)','-1'),(16,'Data Analyst','$48K-$82K (Glassdoor est.)','Analyze basket data and promotion lift.',2.9,'Greenfield Markets2.9','Cincinnati, OH','Cincinnati, OH','10000+ employees',1883,'Company - Private','Grocery Stores & Supermarkets','Retail','$10+ billion (USD)','Harvest Mart, ValueCart'),(17,'Research Scientist','$105K-$158K (Glassdoor est.)','Research signal processing and learning systems.',4.3,'Northgate Research Lab4.3','Lexington, MA','Lexington, MA','1001 to 5000 employees',1951,'College / University','Research & Development','Business Services','$500 million to $1 billion (USD)','-1'),(18,'Data Scientist','$69K-$120K (Glassdoor est.)','n/a',-1,'Harbor Analytics','Portland, OR','-1','1 to 50 employees',-1,'-1','-1','-1','Unknown / Non-Applicable','-1'),(19,'Sr. Data Scientist','$122K-$175K (Glassdoor est.)','Detect fraud patterns across financial products.',4.4,'Finchley Software4.4','San Diego, CA','Mountain View, CA','5001 to 10000 employees',1983,'Company - Private','Computer Hardware & Software','Information Technology','$5 to $10 billion (USD)','Quillsoft, Bytewell'),(20,'Business Intelligence Analyst','$58K-$92K (Glassdoor est.)','Forecast demand for seasonal inventory.',3.4,'Alder & Oak Retail3.4','Seattle, WA','Seattle, WA','10000+ employees',1901,'Company - Private','Department, Clothing, & Shoe Stores','Retail','$10+ billion (USD)','Maple Row, Birch & Co'),(21,'Data Scientist','$84K-$141K (Glassdoor est.)','Deliver machine learning proof of concepts.',3.6,'Slate Advisory3.6','Chicago, IL','Seattle, WA','5001 to 10000 employees',2001,'Company - Private','Consulting','Business Services','$1 to $2 billion (USD)','Ironwood Consulting, Kessler & Co'),(22,'Senior Data Scientist','$132K-$186K (Employer est.)','Model creative workflow and subscription churn.',4.5,'Helix Creative Tools4.5','San Jose, CA','San Jose, CA','10000+ employees',1982,'Company - Public','Computer Hardware & Software','Information Technology','$10+ billion (USD)','Finchley Software, Pixelforge'),(23,'Sr Data Scientist','$95K-$149K (Glassdoor est.)','Price risk using telematics data.',3.8,'Pinnacle Insurance Group3.8','Chevy Chase, MD','Chevy Chase, MD','10000+ employees',1936,'Subsidiary or Business Segment','Insurance Carriers','Insurance','$10+ billion (USD)','Shieldpoint, Covera'),(24,'Data Engineer','$82K-$128K (Employer est.)','Scale search indexing pipelines.',4.1,'Marketbay4.1','Brooklyn, NY','Brooklyn, NY','1001 to 5000 employees',2005,'Company - Private','Internet','Information Technology','$500 million to $1 billion (USD)','Tradewind, Shopnest'),(25,'Research Scientist','$88K-$144K (Glassdoor est.)','Study climate data with statistical models.',-1,'Riverbend Institute','Boulder, CO','Boulder, CO','51 to 200 employees',1990,'Private Practice / Firm','Research & Development','Business Services','Unknown / Non-Applicable','-1'),(26,'Machine Learning Engineer','$118K-$172K (Glassdoor est.)','Rank timelines and detect abuse.',3.7,'Chirp Social3.7','San Francisco, CA','San Francisco, CA','1001 to 5000 employees',2006,'Company - Public','Internet','Information Technology','$1 to $2 billion (USD)','Tweetwave, Loop Social'),(27,'Data Analyst','$55K-$89K (Glassdoor est.)','Track operating room utilization.',4.0,'St. Clair Health System4.0','Boston, MA','Boston, MA','10000+ employees',1994,'Nonprofit Organization','Health Care Services & Hospitals','Health Care','$10+ billion (USD)','-1'),(28,'Senior. Data Scientist -','$126K-$179K (Glassdoor est.)','Model drug discovery experiments.',3.9,'Genova Biosciences3.9','South San Francisco, CA','South San Francisco, CA','10000+ employees',1976,'Subsidiary or Business Segment','Biotech & Pharmaceuticals','Biotech & Pharma','$10+ billion (USD)','Novaline Pharma, Curewell'),(29,'Data Scientist','$72K-$125K (Glassdoor est.)','',-1,'Cedar Health','Denver, CO','Denver, CO','201 to 500 employees',2011,'-1','Health Care Services & Hospitals','Health Care','Unknown / Non-Applicable','-1'),(30,'Business Intelligence Analyst','$50K-$83K (Glassdoor est.)','Maintain reporting dashboards for surveillance data.',3.2,'County Public Health Agency3.2','Atlanta, GA','Atlanta, GA','1001 to 5000 employees',1946,'Government','Federal Agencies','Government','$1 to $2 billion (USD)','-1');",
    "CREATE TABLE ownership_map (raw_label TEXT PRIMARY KEY, clean_label TEXT);",
    "INSERT INTO ownership_map VALUES ('Company - Private','Private'),('Company - Public','Public'),('Nonprofit Organization','Nonprofit'),('Government','Government'),('Subsidiary or Business Segment','Subsidiary'),('College / University','Education'),('Private Practice / Firm','Private');"
  ].join("\n");

  function arenaOpts() {
    return (typeof window !== "undefined" && window.ARENA_OPTS) || {};
  }
  function compatOn() { return !!arenaOpts().pgCompat; }

  /* ---------- PostgreSQL compatibility layer (used by the M7 pages only) ----------
     sql.js runs SQLite, which lacks several PostgreSQL features taught in M7.
     Custom SQL functions cover LEFT/RIGHT/SPLIT_PART/...; a small SQL rewriter
     covers ::casts, START TRANSACTION, POSITION(x IN y), ILIKE, ~ / ~*, TRUNCATE,
     and ALTER COLUMN ... TYPE / SET NOT NULL (done by rebuilding the table). */

  function registerPgFunctions(db) {
    // sql.js takes the SQL arity from fn.length; -1 means "any number of arguments"
    function variadic(name, fn) {
      Object.defineProperty(fn, "length", { value: -1 });
      db.create_function(name, fn);
    }
    function S(v) { return v === null || v === undefined ? null : String(v); }
    db.create_function("left", function (s, n) {
      s = S(s); if (s === null || n === null) return null;
      return n >= 0 ? s.slice(0, n) : s.slice(0, Math.max(0, s.length + n));
    });
    db.create_function("right", function (s, n) {
      s = S(s); if (s === null || n === null) return null;
      return n >= 0 ? s.slice(Math.max(0, s.length - n)) : s.slice(-n);
    });
    db.create_function("split_part", function (s, d, n) {
      s = S(s); d = S(d); if (s === null || d === null || n === null) return null;
      if (n === 0) throw new Error("field position must not be zero");
      var parts = d === "" ? [s] : s.split(d);
      var idx = n > 0 ? n - 1 : parts.length + n;
      return parts[idx] === undefined ? "" : parts[idx];
    });
    db.create_function("strpos", function (s, sub) {
      s = S(s); sub = S(sub); if (s === null || sub === null) return null;
      return s.indexOf(sub) + 1;
    });
    db.create_function("char_length", function (s) { s = S(s); return s === null ? null : s.length; });
    db.create_function("initcap", function (s) {
      s = S(s); if (s === null) return null;
      return s.toLowerCase().replace(/(^|[^a-z0-9])([a-z])/g, function (m, a, b) { return a + b.toUpperCase(); });
    });
    function pad(s, n, fill, left) {
      s = S(s); fill = S(fill); if (s === null || n === null || fill === null) return null;
      if (s.length >= n) return s.slice(0, Math.max(0, n));
      if (fill === "") return s;
      var need = n - s.length, p = "";
      while (p.length < need) p += fill;
      p = p.slice(0, need);
      return left ? p + s : s + p;
    }
    // sql.js registers a function under one name for any argument count, so use optional params
    variadic("lpad", function (s, n, f) { return pad(s, n, f === undefined ? " " : f, true); });
    variadic("rpad", function (s, n, f) { return pad(s, n, f === undefined ? " " : f, false); });
    function mkRe(p, flags) {
      try { return new RegExp(p, flags); } catch (e) { throw new Error("invalid regular expression: " + e.message); }
    }
    db.create_function("regexp", function (p, s) {
      s = S(s); if (s === null || p === null) return null;
      return mkRe(String(p), "").test(s) ? 1 : 0;
    });
    db.create_function("regexpi", function (p, s) {
      s = S(s); if (s === null || p === null) return null;
      return mkRe(String(p), "i").test(s) ? 1 : 0;
    });
    function rre(s, p, r, f) {
      s = S(s); if (s === null || p === null || r === null) return null;
      f = f === null || f === undefined ? "" : String(f);
      var rep = String(r).replace(/\$/g, "$$$$").replace(/\\(\d)/g, "$$$1");
      return s.replace(mkRe(String(p), (f.indexOf("g") >= 0 ? "g" : "") + (f.indexOf("i") >= 0 ? "i" : "")), rep);
    }
    variadic("regexp_replace", function (s, p, r, f) { return rre(s, p, r, f); });
    db.create_function("regexp_substr", function (s, p) {
      s = S(s); if (s === null || p === null) return null;
      var m = mkRe(String(p), "").exec(s);
      if (!m) return null;
      return m.length > 1 ? (m[1] === undefined ? null : m[1]) : m[0];
    });
  }

  // Replaces comments with a space and string/identifier literals with \x01N\x01 placeholders.
  function pgTokenize(sql) {
    var strings = [], out = "", i = 0, n = sql.length;
    while (i < n) {
      var c = sql[i], d = sql[i + 1];
      if (c === "-" && d === "-") { while (i < n && sql[i] !== "\n") i++; out += " "; continue; }
      if (c === "/" && d === "*") { var e = sql.indexOf("*/", i + 2); i = e === -1 ? n : e + 2; out += " "; continue; }
      if (c === "'" || c === '"') {
        var j = i + 1;
        while (j < n) {
          if (sql[j] === c) { if (sql[j + 1] === c) { j += 2; continue; } break; }
          j++;
        }
        strings.push(sql.slice(i, j + 1));
        out += "\x01" + (strings.length - 1) + "\x01";
        i = j + 1; continue;
      }
      out += c; i++;
    }
    return { code: out, strings: strings };
  }
  function pgRestore(code, strings) {
    return code.replace(/\x01(\d+)\x01/g, function (m, k) { return strings[+k]; });
  }
  function pgFindClose(code, openIdx) {
    var depth = 0;
    for (var i = openIdx; i < code.length; i++) {
      if (code[i] === "(") depth++;
      else if (code[i] === ")") { depth--; if (depth === 0) return i; }
    }
    return -1;
  }
  // index of a top-level (depth 0) occurrence of the regex `re` in `s`, or -1
  function pgTopLevelIndex(s, re) {
    var depth = 0;
    for (var i = 0; i < s.length; i++) {
      if (s[i] === "(") depth++;
      else if (s[i] === ")") depth--;
      else if (depth === 0) {
        var m = re.exec(s.slice(i));
        if (m && m.index === 0) return { idx: i, len: m[0].length };
      }
    }
    return null;
  }
  function pgSplitTop(s, sep) {
    var parts = [], depth = 0, cur = "";
    for (var i = 0; i < s.length; i++) {
      var c = s[i];
      if (c === "(") depth++;
      else if (c === ")") depth--;
      if (c === sep && depth === 0) { parts.push(cur); cur = ""; } else cur += c;
    }
    parts.push(cur);
    return parts;
  }
  function pgRewriteFunc(code, name, rewriter) {
    var re = new RegExp("\\b" + name + "\\s*\\(", "gi"), from = 0, m;
    while ((m = (re.lastIndex = from, re.exec(code)))) {
      var open = m.index + m[0].length - 1, close = pgFindClose(code, open);
      if (close === -1) break;
      var inner = code.slice(open + 1, close), repl = rewriter(inner);
      if (repl === null) { from = m.index + m[0].length; continue; }
      code = code.slice(0, m.index) + repl + code.slice(close + 1);
      from = m.index + repl.length;
    }
    return code;
  }
  function pgRewriteCasts(code) {
    for (var guard = 0; guard < 60; guard++) {
      var k = code.indexOf("::");
      if (k === -1) break;
      var j = k - 1;
      while (j >= 0 && /\s/.test(code[j])) j--;
      var end = j + 1, start;
      if (code[j] === ")") {
        var depth = 0;
        for (start = j; start >= 0; start--) {
          if (code[start] === ")") depth++;
          else if (code[start] === "(") { depth--; if (depth === 0) break; }
        }
        var f = start - 1;
        while (f >= 0 && /[\w.]/.test(code[f])) f--;
        start = f + 1;
      } else if (code[j] === "\x01") {
        start = code.lastIndexOf("\x01", j - 1);
      } else {
        start = j;
        while (start >= 0 && /[\w.]/.test(code[start])) start--;
        start++;
      }
      var operand = code.slice(start, end);
      var rest = code.slice(k + 2), tm = rest.match(/^\s*([A-Za-z_]\w*(?:\s*\(\s*\d+(?:\s*,\s*\d+)?\s*\))?)/);
      if (!tm || !operand) { code = code.slice(0, k) + "\x02" + code.slice(k + 2); continue; }
      code = code.slice(0, start) + "CAST(" + operand + " AS " + tm[1] + ")" + rest.slice(tm[0].length);
    }
    return code.replace(/\x02/g, "::");
  }
  function pgRewrite(code) {
    code = code.replace(/\bSTART\s+TRANSACTION\b/gi, "BEGIN").replace(/\bILIKE\b/gi, "LIKE");
    code = pgRewriteFunc(code, "POSITION", function (inner) {
      var hit = pgTopLevelIndex(inner, /^\s+IN\s+/i);
      if (!hit) return null;
      return "INSTR(" + inner.slice(hit.idx + hit.len).trim() + ", " + inner.slice(0, hit.idx).trim() + ")";
    });
    code = pgRewriteFunc(code, "SUBSTRING", function (inner) {
      var hit = pgTopLevelIndex(inner, /^\s+FROM\s+/i);
      if (!hit) return null;
      var x = inner.slice(0, hit.idx).trim(), rest = inner.slice(hit.idx + hit.len).trim();
      var f = pgTopLevelIndex(rest, /^\s+FOR\s+/i);
      if (f) return "SUBSTR(" + x + ", " + rest.slice(0, f.idx).trim() + ", " + rest.slice(f.idx + f.len).trim() + ")";
      if (rest.charAt(0) === "\x01") return "REGEXP_SUBSTR(" + x + ", " + rest + ")";
      return "SUBSTR(" + x + ", " + rest + ")";
    });
    code = pgRewriteCasts(code);
    code = code.replace(/((?:[A-Za-z_][\w.]*(?:\s*\([^()]*\))?))\s*(!?~\*?)\s*(\x01\d+\x01)/g, function (m, operand, op, ph) {
      return (op.charAt(0) === "!" ? "NOT " : "") + (op.indexOf("*") >= 0 ? "regexpi" : "regexp") + "(" + ph + ", " + operand + ")";
    });
    return code;
  }

  var PG_NUMERIC_TYPE = /^(int|integer|bigint|smallint|int2|int4|int8|numeric|decimal|real|float|double)/i;
  var PG_INT_TYPE = /^(int|integer|bigint|smallint|int2|int4|int8)$/i;
  function pgUnquote(id) { return String(id).replace(/^"|"$/g, ""); }

  // SQLite cannot change a column type / NOT NULL in place, so rebuild the table.
  function pgRebuild(db, table, col, opts) {
    table = pgUnquote(table); col = pgUnquote(col);
    var info = db.exec('SELECT cid, name, type, "notnull", dflt_value, pk FROM pragma_table_info(\'' + table.replace(/'/g, "''") + "') ORDER BY cid");
    if (!info.length) throw new Error('relation "' + table + '" does not exist');
    var cols = info[0].values.map(function (r) { return { name: r[1], type: r[2], notnull: r[3], dflt: r[4], pk: r[5] }; });
    var target = null;
    cols.forEach(function (c) { if (c.name.toLowerCase() === col.toLowerCase()) target = c; });
    if (!target) throw new Error('column "' + col + '" of relation "' + table + '" does not exist');
    var q = function (n) { return '"' + n + '"'; };
    var expr = opts.using ? opts.using : q(target.name);
    if (opts.type && PG_NUMERIC_TYPE.test(opts.type)) {
      var inner = /^CAST\(([\s\S]*)\s+AS\s+[A-Za-z_]\w*(?:\s*\(\s*\d+(?:\s*,\s*\d+)?\s*\))?\)$/i.exec(expr.trim());
      var chk = db.exec("SELECT " + (inner ? inner[1] : expr) + " AS v FROM " + q(table));
      var isInt = PG_INT_TYPE.test(opts.type.replace(/\s*\(.*$/, ""));
      var okRe = isInt ? /^\s*[-+]?\d+\s*$/ : /^\s*[-+]?(\d+(\.\d*)?|\.\d+)\s*$/;
      if (chk.length) {
        for (var i = 0; i < chk[0].values.length; i++) {
          var v = chk[0].values[i][0];
          if (v !== null && typeof v === "string" && !okRe.test(v)) {
            throw new Error('invalid input syntax for type ' + opts.type.toLowerCase() + ': "' + v + '"');
          }
        }
      }
    }
    var tmp = table + "__rebuild";
    var defs = cols.map(function (c) {
      var isT = c === target;
      var type = isT && opts.type ? opts.type : c.type;
      var nn = isT && opts.notnull !== undefined ? opts.notnull : c.notnull;
      return q(c.name) + (type ? " " + type : "") + (nn ? " NOT NULL" : "") + (c.dflt !== null ? " DEFAULT " + c.dflt : "");
    });
    var pks = cols.filter(function (c) { return c.pk > 0; }).sort(function (a, b) { return a.pk - b.pk; });
    if (pks.length) defs.push("PRIMARY KEY (" + pks.map(function (c) { return q(c.name); }).join(", ") + ")");
    var sel = cols.map(function (c) {
      if (c === target && opts.type) return "CAST(" + expr + " AS " + opts.type + ") AS " + q(c.name);
      return q(c.name);
    });
    db.exec("CREATE TABLE " + q(tmp) + " (" + defs.join(", ") + ")");
    try {
      db.exec("INSERT INTO " + q(tmp) + " SELECT " + sel.join(", ") + " FROM " + q(table));
    } catch (e) {
      db.exec("DROP TABLE " + q(tmp));
      if (/NOT NULL/i.test(e.message)) throw new Error('column "' + col + '" of relation "' + table + '" contains null values');
      throw e;
    }
    db.exec("DROP TABLE " + q(table));
    db.exec("ALTER TABLE " + q(tmp) + " RENAME TO " + q(table));
  }

  var PG_TYPE_EXPR = "([A-Za-z_]\\w*(?:\\s*\\(\\s*\\d+(?:\\s*,\\s*\\d+)?\\s*\\))?)";
  function pgAlterAction(db, table, action, strings) {
    var R = function (s) { return pgRestore(s, strings); };
    var m = action.match(new RegExp("^ALTER\\s+(?:COLUMN\\s+)?(\\S+)\\s+(?:SET\\s+DATA\\s+)?TYPE\\s+" + PG_TYPE_EXPR + "(?:\\s+USING\\s+([\\s\\S]+))?$", "i"));
    if (m) { pgRebuild(db, table, m[1], { type: m[2], using: m[3] ? R(m[3]) : null }); return; }
    m = action.match(/^ALTER\s+(?:COLUMN\s+)?(\S+)\s+SET\s+NOT\s+NULL$/i);
    if (m) { pgRebuild(db, table, m[1], { notnull: 1 }); return; }
    m = action.match(/^ALTER\s+(?:COLUMN\s+)?(\S+)\s+DROP\s+NOT\s+NULL$/i);
    if (m) { pgRebuild(db, table, m[1], { notnull: 0 }); return; }
    db.exec("ALTER TABLE " + table + " " + R(action));
  }

  // Runs one (placeholder-form) statement; returns the latest row-producing result.
  function pgRunStatement(db, stmt, strings, last) {
    var R = function (s) { return pgRestore(s, strings); };
    var m = stmt.match(/^TRUNCATE(?:\s+TABLE)?\s+(?:ONLY\s+)?(\S+?)(?:\s+RESTART\s+IDENTITY)?(?:\s+CASCADE)?$/i);
    if (m) stmt = "DELETE FROM " + m[1];
    var at = stmt.match(/^ALTER\s+TABLE\s+(?:IF\s+EXISTS\s+)?(?:ONLY\s+)?(\S+)\s+([\s\S]+)$/i);
    if (at && !/^(RENAME|ADD|DROP)\s/i.test(at[2].trim()) || (at && pgSplitTop(at[2], ",").length > 1)) {
      pgSplitTop(at[2], ",").forEach(function (a) { pgAlterAction(db, at[1], a.trim(), strings); });
      return last;
    }
    var res = db.exec(R(stmt));
    if (res.length) return { columns: res[res.length - 1].columns, rows: res[res.length - 1].values };
    return last;
  }

  function pgExecScript(db, sql) {
    var tk = pgTokenize(sql);
    var code = pgRewrite(tk.code);
    var last = { columns: [], rows: [] };
    code.split(";").forEach(function (raw) {
      var stmt = raw.trim();
      if (stmt) last = pgRunStatement(db, stmt, tk.strings, last);
    });
    return last;
  }

  function openDb() {
    var db = new SQLlib.Database(pristineBytes);
    if (compatOn()) registerPgFunctions(db);
    return db;
  }
  function runScript(db, sql) {
    if (compatOn()) return pgExecScript(db, sql);
    var res = db.exec(sql);
    return res.length === 0 ? { columns: [], rows: [] } : { columns: res[0].columns, rows: res[0].values };
  }

  function init() {
    if (readyPromise) return readyPromise;
    readyPromise = initSqlJs({
      locateFile: function (file) {
        return "https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.14.2/" + file;
      }
    }).then(function (SQL) {
      SQLlib = SQL;
      var db = new SQL.Database();
      db.run(SEED_SQL);
      pristineBytes = db.export();
      db.close();
      return true;
    });
    return readyPromise;
  }

  var NOT_READY = "SQLエンジンを読み込み中です。少し待ってからもう一度お試しください。";

  // Runs `sql` against a fresh copy of the seeded DB. Never mutates shared state.
  function runQuery(sql) {
    if (!SQLlib || !pristineBytes) return { error: NOT_READY };
    var db = openDb();
    try {
      var out = runScript(db, sql);
      db.close();
      return out;
    } catch (e) {
      db.close();
      return { error: e.message };
    }
  }

  // Runs a mutating script, then a verification query on the SAME fresh DB.
  function runMutationPreview(script, verifySql) {
    if (!SQLlib || !pristineBytes) return { error: NOT_READY };
    var db = openDb();
    try {
      var scriptRes = runScript(db, script);
      var state = runScript(db, verifySql);
      db.close();
      return { script: scriptRes.rows.length ? scriptRes : null, state: state };
    } catch (e) {
      db.close();
      return { error: e.message };
    }
  }

  function normalizeRows(rows) {
    return rows.map(function (r) {
      return r.map(function (v) { return v === null ? "∅" : String(v); });
    });
  }

  function compareRows(aRows, bRows, orderSensitive) {
    var a = normalizeRows(aRows).map(function (r) { return r.join("\u0001"); });
    var b = normalizeRows(bRows).map(function (r) { return r.join("\u0001"); });
    if (!orderSensitive) { a.sort(); b.sort(); }
    var pass = JSON.stringify(a) === JSON.stringify(b);
    var diff = 0;
    if (!pass) {
      var pool = {};
      b.forEach(function (x) { pool[x] = (pool[x] || 0) + 1; });
      a.forEach(function (x) { if (pool[x]) pool[x]--; else diff++; });
      diff = Math.max(diff, Math.abs(a.length - b.length));
    }
    return { pass: pass, diff: diff };
  }

  function gradeQuery(studentSql, solutionSql, orderSensitive) {
    var student = runQuery(studentSql);
    if (student.error) {
      return { pass: false, studentError: student.error, student: null, expected: null };
    }
    var expected = runQuery(solutionSql);
    if (expected.error) {
      return { pass: false, studentError: null, engineError: expected.error, student: student, expected: null };
    }
    var c = compareRows(student.rows, expected.rows, orderSensitive);
    return { pass: c.pass, diff: c.diff, student: student, expected: expected };
  }

  function stripForKeywordCheck(sql) {
    return pgTokenize(sql).code;
  }

  // Mutate-then-verify grading: run the student's script and the model script on
  // separate fresh DBs, then compare the result of the same verification SELECT.
  function gradeMutation(studentSql, solutionSql, verifySql, orderSensitive, requireKeywords) {
    if (requireKeywords && requireKeywords.length) {
      var code = stripForKeywordCheck(studentSql);
      for (var i = 0; i < requireKeywords.length; i++) {
        if (!new RegExp("\\b" + requireKeywords[i].replace(/\s+/g, "\\s+") + "\\b", "i").test(code)) {
          return { pass: false, missingKeyword: requireKeywords[i], student: null, expected: null };
        }
      }
    }
    var s = runMutationPreview(studentSql, verifySql);
    if (s.error) return { pass: false, studentError: s.error, student: null, expected: null };
    var e = runMutationPreview(solutionSql, verifySql);
    if (e.error) return { pass: false, engineError: e.error, student: s.state, expected: null };
    var c = compareRows(s.state.rows, e.state.rows, orderSensitive);
    return { pass: c.pass, diff: c.diff, student: s.state, expected: e.state };
  }

  return { init: init, runQuery: runQuery, gradeQuery: gradeQuery, runMutationPreview: runMutationPreview, gradeMutation: gradeMutation };
})();

/* ===== Live syntax highlighting (textarea-over-pre overlay, SQL tokenizer) ===== */

var SQL_KEYWORDS = ["SELECT","FROM","WHERE","JOIN","INNER","LEFT","RIGHT","FULL","OUTER","CROSS",
  "ON","USING","GROUP","BY","ORDER","HAVING","AS","AND","OR","NOT","IN","IS","NULL","NULLS",
  "UNION","ALL","INTERSECT","EXCEPT","DISTINCT","CASE","WHEN","THEN","ELSE","END","WITH",
  "LIMIT","ASC","DESC","BETWEEN","LIKE","EXISTS","CAST","COUNT","SUM","AVG","MIN","MAX",
  "INSERT","INTO","VALUES","UPDATE","SET","DELETE","CREATE","TABLE","PRIMARY","KEY",
  "FOREIGN","REFERENCES","CHECK","DEFAULT","UNIQUE",
  "ALTER","ADD","COLUMN","DROP","RENAME","TO","BEGIN","COMMIT","ROLLBACK","TRANSACTION","START",
  "RETURNING","TRUNCATE","USING","DATA","TYPE","ILIKE","IF","TRIM","LENGTH","REPLACE","SUBSTR","SUBSTRING",
  "SPLIT_PART","STRPOS","POSITION","INSTR","UPPER","LOWER","INITCAP","CHAR_LENGTH","LPAD","RPAD",
  "REGEXP","REGEXP_REPLACE","COALESCE","NULLIF","CONCAT","ROUND","GROUP_CONCAT","STRING_AGG","LIMIT","OFFSET","TEMP","VIEW","INDEX"];
var SQL_TYPES = ["INTEGER","INT","BIGINT","TEXT","NUMERIC","DECIMAL","REAL","FLOAT","VARCHAR","CHAR","DATE","BOOLEAN","MONEY"];

/* Table/column names available for autocomplete — must match SEED_SQL above. */
var SCHEMA_INFO = {
  department: ["dept_name", "building", "budget"],
  instructor: ["instructor_id", "name", "dept_name", "salary"],
  student: ["student_id", "name", "dept_name", "tot_cred"],
  course: ["course_id", "title", "dept_name", "credits"],
  section: ["course_id", "section_id", "semester", "year", "building", "room_number"],
  takes: ["student_id", "course_id", "section_id", "semester", "year", "grade"],
  teaches: ["instructor_id", "course_id", "section_id", "semester", "year"],
  advisor: ["student_id", "instructor_id"],
  prereq: ["course_id", "prereq_id"],
  branch: ["branch_name", "branch_city", "assets"],
  customer: ["customer_id", "customer_name", "customer_street", "customer_city"],
  account: ["account_number", "branch_name", "balance"],
  depositor: ["customer_id", "account_number"],
  loan: ["loan_number", "branch_name", "amount"],
  borrower: ["customer_id", "loan_number"],
  ds_jobs: ["post_id", "job_title", "salary_estimate", "job_description", "rating", "company_name", "location", "headquarters", "size", "founded", "type_of_ownership", "industry", "sector", "revenue", "competitors"],
  ownership_map: ["raw_label", "clean_label"]
};
var SCHEMA_TYPES = {
  ds_jobs: ["INTEGER PK", "TEXT", "TEXT", "TEXT", "REAL", "TEXT", "TEXT", "TEXT", "TEXT", "INTEGER", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT"],
  ownership_map: ["TEXT PK", "TEXT"]
};
var SCHEMA_GROUP_DEFS = {
  university: { title: "🎓 University DB", tables: ["department", "instructor", "student", "course", "section", "takes", "teaches", "advisor", "prereq"] },
  banking: { title: "🏦 Banking DB", tables: ["branch", "customer", "account", "depositor", "loan", "borrower"] },
  ds_jobs: { title: "📊 求人データ（ds_jobs）", tables: ["ds_jobs", "ownership_map"] }
};
function activeSchemaGroups() {
  var g = (typeof window !== "undefined" && window.ARENA_OPTS && window.ARENA_OPTS.schemaGroups) || ["university", "banking"];
  return g.filter(function (k) { return SCHEMA_GROUP_DEFS[k]; });
}
function activeSchemaTables() {
  var out = [];
  activeSchemaGroups().forEach(function (k) { out = out.concat(SCHEMA_GROUP_DEFS[k].tables); });
  return out;
}
function activeSchemaColumns() {
  var seen = {}, list = [];
  activeSchemaTables().forEach(function (t) {
    (SCHEMA_INFO[t] || []).forEach(function (c) { if (!seen[c]) { seen[c] = true; list.push(c); } });
  });
  return list;
}
var SCHEMA_TABLES = Object.keys(SCHEMA_INFO);
var SCHEMA_COLUMNS = (function () {
  var seen = {}, list = [];
  SCHEMA_TABLES.forEach(function (t) {
    SCHEMA_INFO[t].forEach(function (c) {
      if (!seen[c]) { seen[c] = true; list.push(c); }
    });
  });
  return list;
})();

function escapeHtmlSQL(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function highlightSQLLine(line) {
  var out = "", i = 0;
  while (i < line.length) {
    var rest = line.slice(i);
    if (rest.slice(0, 2) === "--") {
      out += '<span class="cm">' + escapeHtmlSQL(rest) + "</span>";
      break;
    }
    var m = rest.match(/^'[^']*'/) || rest.match(/^"[^"]*"/);
    if (m) {
      out += '<span class="st">' + escapeHtmlSQL(m[0]) + "</span>";
      i += m[0].length;
      continue;
    }
    m = rest.match(/^-?\d+(\.\d+)?/);
    if (m) {
      out += '<span class="nm">' + escapeHtmlSQL(m[0]) + "</span>";
      i += m[0].length;
      continue;
    }
    m = rest.match(/^[A-Za-z_]\w*/);
    if (m) {
      var w = m[0], up = w.toUpperCase();
      if (SQL_KEYWORDS.indexOf(up) !== -1 || SQL_TYPES.indexOf(up) !== -1) {
        out += '<span class="kw">' + escapeHtmlSQL(w) + "</span>";
      } else {
        out += escapeHtmlSQL(w);
      }
      i += w.length;
      continue;
    }
    out += escapeHtmlSQL(rest[0]);
    i += 1;
  }
  return out;
}

function highlightSQL(code) {
  return code.split("\n").map(highlightSQLLine).join("\n");
}

/* ===== Autocomplete (keywords + table/column names) ===== */

var AC = { open: false, editorId: null, items: [], active: 0, dropdownEl: null };

function acGetWordRangeAtCaret(editor) {
  var pos = editor.selectionStart, val = editor.value;
  var start = pos;
  while (start > 0 && /[A-Za-z0-9_]/.test(val[start - 1])) start--;
  return { start: start, end: pos, word: val.slice(start, pos) };
}

// Classic "mirror div" technique: clone the textarea's box/font metrics onto an
// offscreen div containing the text up to the caret, then read where that text
// ends to know the caret's on-screen pixel position.
function acGetCaretCoordinates(textarea, position) {
  var mirror = document.createElement("div");
  var style = getComputedStyle(textarea);
  ["boxSizing", "width", "paddingTop", "paddingRight", "paddingBottom", "paddingLeft",
   "borderTopWidth", "borderRightWidth", "borderBottomWidth", "borderLeftWidth",
   "fontFamily", "fontSize", "fontWeight", "lineHeight", "letterSpacing", "whiteSpace"]
    .forEach(function (p) { mirror.style[p] = style[p]; });
  mirror.style.position = "absolute";
  mirror.style.visibility = "hidden";
  mirror.style.top = "0";
  mirror.style.left = "-9999px";
  document.body.appendChild(mirror);
  mirror.textContent = textarea.value.substring(0, position);
  var span = document.createElement("span");
  span.textContent = textarea.value.substring(position) || ".";
  mirror.appendChild(span);
  var coords = { top: span.offsetTop, left: span.offsetLeft, height: span.offsetHeight || parseInt(style.lineHeight, 10) || 18 };
  document.body.removeChild(mirror);
  return coords;
}

function acGetDropdown() {
  if (!AC.dropdownEl) {
    AC.dropdownEl = document.createElement("div");
    AC.dropdownEl.className = "autocomplete-dropdown";
    AC.dropdownEl.hidden = true;
    document.body.appendChild(AC.dropdownEl);
  }
  return AC.dropdownEl;
}

function acHide() {
  AC.open = false;
  AC.editorId = null;
  if (AC.dropdownEl) AC.dropdownEl.hidden = true;
}

function acCandidateTag(word) {
  var up = word.toUpperCase();
  if (SQL_TYPES.indexOf(up) !== -1) return "type";
  if (SQL_KEYWORDS.indexOf(up) !== -1) return "keyword";
  if (activeSchemaTables().indexOf(word) !== -1) return "table";
  return "column";
}

function acUpdate(editorId) {
  var editor = document.getElementById("ed-" + editorId);
  var range = acGetWordRangeAtCaret(editor);
  if (range.word.length < 1) { acHide(); return; }
  var upper = range.word.toUpperCase();
  var lower = range.word.toLowerCase();
  var kwMatches = SQL_KEYWORDS.concat(SQL_TYPES).filter(function (k) {
    return k.indexOf(upper) === 0;
  });
  var nameMatches = activeSchemaTables().concat(activeSchemaColumns()).filter(function (n) {
    return n.toLowerCase().indexOf(lower) === 0;
  });
  var seen = {};
  var items = [];
  kwMatches.concat(nameMatches).forEach(function (text) {
    if (seen[text]) return;
    seen[text] = true;
    items.push({ text: text, tag: acCandidateTag(text) });
  });
  items = items.slice(0, 8);
  if (items.length === 0 || (items.length === 1 && items[0].text.toLowerCase() === lower)) { acHide(); return; }
  AC.open = true;
  AC.editorId = editorId;
  AC.items = items;
  AC.active = 0;
  acRender(editor, range);
}

var AC_TAG_LABEL = { keyword: "keyword", type: "type", table: "table", column: "column" };

function acRender(editor, range) {
  var dd = acGetDropdown();
  dd.innerHTML = "";
  AC.items.forEach(function (item, idx) {
    var el = document.createElement("div");
    el.className = "autocomplete-item" + (idx === AC.active ? " active" : "");
    el.innerHTML = "<span>" + escapeHtmlSQL(item.text) + '</span><span class="ac-tag">' + AC_TAG_LABEL[item.tag] + "</span>";
    el.addEventListener("mousedown", function (e) {
      e.preventDefault();
      acApply(idx);
    });
    dd.appendChild(el);
  });
  var coords = acGetCaretCoordinates(editor, range.end);
  var rect = editor.getBoundingClientRect();
  dd.style.left = (rect.left + window.scrollX + coords.left - editor.scrollLeft) + "px";
  dd.style.top = (rect.top + window.scrollY + coords.top + coords.height - editor.scrollTop) + "px";
  dd.hidden = false;
}

function acApply(idx) {
  if (!AC.open || !AC.editorId) return;
  var editor = document.getElementById("ed-" + AC.editorId);
  var range = acGetWordRangeAtCaret(editor);
  var chosen = AC.items[idx !== undefined ? idx : AC.active];
  if (!chosen) return;
  var before = editor.value.slice(0, range.start), after = editor.value.slice(range.end);
  editor.value = before + chosen.text + after;
  var newPos = before.length + chosen.text.length;
  editor.selectionStart = editor.selectionEnd = newPos;
  editor.dispatchEvent(new Event("input"));
  acHide();
  editor.focus();
}

document.addEventListener("scroll", function () { if (AC.open) acHide(); }, true);
document.addEventListener("mousedown", function (e) {
  if (AC.open && AC.dropdownEl && !AC.dropdownEl.contains(e.target)) acHide();
});

/* ===== Result table rendering ===== */

function renderResultTable(result) {
  if (result.error) {
    return '<div class="sql-error">⚠️ ' + escapeHtmlSQL(result.error) + "</div>";
  }
  if (!result.rows || result.rows.length === 0) {
    return '<div class="sql-empty">（結果は0行でした）</div>';
  }
  var html = '<div class="result-wrap"><table class="result-table"><thead><tr>';
  result.columns.forEach(function (c) { html += "<th>" + escapeHtmlSQL(c) + "</th>"; });
  html += "</tr></thead><tbody>";
  result.rows.slice(0, 50).forEach(function (row) {
    html += "<tr>";
    row.forEach(function (v) {
      html += "<td>" + (v === null ? '<span class="null-val">NULL</span>' : escapeHtmlSQL(String(v))) + "</td>";
    });
    html += "</tr>";
  });
  html += "</tbody></table>";
  if (result.rows.length > 50) {
    html += '<div class="sql-empty">（' + result.rows.length + "行中、先頭50行のみ表示）</div>";
  }
  html += "</div>";
  return html;
}

/* ===== Practice card rendering + wiring ===== */

function buildPracticeCard(p) {
  var card = document.createElement("div");
  card.className = "practice-card sql-practice-card";
  card.innerHTML =
    '<div class="ptitle">' + escapeHtmlSQL(p.title) + ' <span class="ptier">' + p.tier + "</span></div>" +
    '<p class="ptask">' + p.scenario + "</p>" +
    '<p class="pconcept">🎯 <strong>スキル:</strong> ' + escapeHtmlSQL(p.concept) + "</p>" +
    (p.mode === "mutate"
      ? '<p class="pmode">🧪 <strong>更新系の問題：</strong>▶実行で更新後のテーブルの状態を確認でき、✅採点は「更新後のテーブルの状態」を模範解答と比べます。</p>'
      : "") +
    '<div class="editor-wrap">' +
      '<pre class="code-highlight" id="hl-' + p.id + '" aria-hidden="true"><code></code></pre>' +
      '<textarea class="code-editor" id="ed-' + p.id + '" spellcheck="false" wrap="off"></textarea>' +
    "</div>" +
    '<div class="practice-toolbar">' +
      '<button class="run-btn" type="button" data-id="' + p.id + '">▶ 実行</button>' +
      '<button class="check-btn" type="button" data-id="' + p.id + '">✅ 採点</button>' +
      '<button class="hint-btn" type="button" data-id="' + p.id + '">💡 ヒントを見る</button>' +
      '<button class="reveal-btn" type="button" data-id="' + p.id + '">🔑 答えを見る</button>' +
    "</div>" +
    '<div class="check-result" id="result-' + p.id + '"></div>' +
    '<p class="phint" id="hint-' + p.id + '" hidden>💡 <strong>ヒント:</strong> ' + escapeHtmlSQL(p.hint) + "</p>" +
    '<div class="answer-reveal" id="answer-' + p.id + '" hidden>' +
      '<pre class="code-block"><code id="answer-code-' + p.id + '"></code></pre>' +
    "</div>";
  return card;
}

function wirePracticeCard(p) {
  var editor = document.getElementById("ed-" + p.id);
  var hl = document.getElementById("hl-" + p.id);
  var hlCode = hl.querySelector("code");
  editor.value = p.starter;

  function sync() {
    hlCode.innerHTML = highlightSQL(editor.value) + "\n";
  }
  sync();
  editor.addEventListener("input", function () {
    sync();
    acUpdate(p.id);
  });
  editor.addEventListener("scroll", function () {
    hl.scrollTop = editor.scrollTop;
    hl.scrollLeft = editor.scrollLeft;
    if (AC.open && AC.editorId === p.id) acHide();
  });
  editor.addEventListener("blur", function () {
    // Small delay so a mousedown on a dropdown item still registers as a click
    // before we hide it (blur fires before the item's own click otherwise).
    setTimeout(function () { if (AC.editorId === p.id) acHide(); }, 150);
  });
  editor.addEventListener("keydown", function (e) {
    if (AC.open && AC.editorId === p.id) {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        AC.active = (AC.active + 1) % AC.items.length;
        acRender(editor, acGetWordRangeAtCaret(editor));
        return;
      }
      if (e.key === "ArrowUp") {
        e.preventDefault();
        AC.active = (AC.active - 1 + AC.items.length) % AC.items.length;
        acRender(editor, acGetWordRangeAtCaret(editor));
        return;
      }
      if (e.key === "Tab" || e.key === "Enter") {
        e.preventDefault();
        acApply();
        return;
      }
      if (e.key === "Escape") {
        e.preventDefault();
        acHide();
        return;
      }
    }
    if (e.key === "Tab") {
      e.preventDefault();
      var s = editor.selectionStart, en = editor.selectionEnd;
      editor.value = editor.value.slice(0, s) + "  " + editor.value.slice(en);
      editor.selectionStart = editor.selectionEnd = s + 2;
      editor.dispatchEvent(new Event("input"));
    }
  });

  var runBtn = document.querySelector('.run-btn[data-id="' + p.id + '"]');
  var checkBtn = document.querySelector('.check-btn[data-id="' + p.id + '"]');
  var hintBtn = document.querySelector('.hint-btn[data-id="' + p.id + '"]');
  var revealBtn = document.querySelector('.reveal-btn[data-id="' + p.id + '"]');
  var resultEl = document.getElementById("result-" + p.id);
  var hintEl = document.getElementById("hint-" + p.id);
  var answerEl = document.getElementById("answer-" + p.id);
  var answerCodeEl = document.getElementById("answer-code-" + p.id);
  answerCodeEl.innerHTML = highlightSQL(p.solution);

  function hasSql(text) {
    // ignore both "-- line" and "/* block */" comments when checking that something was typed
    return text.replace(/\/\*[\s\S]*?(\*\/|$)/g, "").replace(/--[^\n]*/g, "").trim() !== "";
  }

  runBtn.addEventListener("click", function () {
    if (p.mode === "mutate") {
      var pv = SQL_ENGINE.runMutationPreview(editor.value, p.verify);
      if (pv.error) {
        resultEl.innerHTML = '<div class="result-label">▶ 実行結果</div>' + renderResultTable({ error: pv.error });
        return;
      }
      var html = "";
      if (pv.script) html += '<div class="result-label">▶ 実行結果（RETURNING／SELECTの出力）</div>' + renderResultTable(pv.script);
      html += '<div class="result-label">📋 実行後のテーブルの状態</div>' + renderResultTable(pv.state);
      resultEl.innerHTML = html;
      return;
    }
    var res = SQL_ENGINE.runQuery(editor.value);
    resultEl.innerHTML = '<div class="result-label">▶ 実行結果</div>' + renderResultTable(res);
  });

  checkBtn.addEventListener("click", function () {
    if (!hasSql(editor.value)) {
      resultEl.innerHTML = '<div class="check-result-msg fail">✍️ まずSQLを入力してから採点してください。</div>';
      return;
    }
    var mutate = p.mode === "mutate";
    var g = mutate
      ? SQL_ENGINE.gradeMutation(editor.value, p.solution, p.verify, !!p.orderSensitive, p.requireKeywords)
      : SQL_ENGINE.gradeQuery(editor.value, p.solution, !!p.orderSensitive);
    var html = "";
    var label = mutate ? "📋 あなたの実行後のテーブルの状態" : "▶ あなたの実行結果";
    if (g.missingKeyword) {
      html += '<div class="check-result-msg fail">⚠️ この問題では <code>' + escapeHtmlSQL(g.missingKeyword) + '</code> を使う必要があります。SQLに含まれていません。</div>';
    } else if (g.studentError) {
      html += '<div class="check-result-msg fail">❌ SQLエラー: ' + escapeHtmlSQL(g.studentError) + "</div>";
    } else if (g.pass) {
      html += '<div class="check-result-msg pass">✅ 正解です！' + (mutate ? "更新後のテーブルの状態が模範解答と一致しました。" : "結果が模範解答と一致しました。") + "</div>";
      html += '<div class="result-label">' + (mutate ? "📋 更新後のテーブルの状態" : "▶ 実行結果") + "</div>" + renderResultTable(g.student);
    } else {
      html += '<div class="check-result-msg fail">❌ ' + (mutate ? "更新後のテーブルの状態が模範解答と一致しません" : "結果が模範解答と一致しません") +
        (mutate && g.diff ? "（一致しない行：約" + g.diff + "行）" : "") + "。もう一度見直してみましょう。</div>";
      html += '<div class="result-label">' + label + "</div>" + renderResultTable(g.student);
    }
    resultEl.innerHTML = html;
  });

  hintBtn.addEventListener("click", function () {
    hintEl.hidden = !hintEl.hidden;
    hintBtn.textContent = hintEl.hidden ? "💡 ヒントを見る" : "🙈 ヒントを隠す";
  });

  revealBtn.addEventListener("click", function () {
    answerEl.hidden = !answerEl.hidden;
    revealBtn.textContent = answerEl.hidden ? "🔑 答えを見る" : "🙈 答えを隠す";
  });
}

/* ===== Schema reference panel (which tables/columns exist) ===== */

function schemaTableRow(t) {
  var types = SCHEMA_TYPES[t];
  var cols = SCHEMA_INFO[t].map(function (c, i) { return types ? c + " " + types[i] : c; });
  return '<div class="schema-table"><span class="schema-tname">' + escapeHtmlSQL(t) + "</span>" +
    '<span class="schema-cols">' + escapeHtmlSQL(cols.join(", ")) + "</span></div>";
}

function buildSchemaRefHTML() {
  var groups = activeSchemaGroups();
  return '<div class="schema-ref" id="schemaRef">' +
    '<button type="button" class="schema-ref-toggle" id="schemaRefToggle">📋 テーブル構成（列一覧）を見る ▾</button>' +
    '<div class="schema-ref-body' + (groups.length === 1 ? " single" : "") + '" id="schemaRefBody" hidden>' +
      groups.map(function (k) {
        var def = SCHEMA_GROUP_DEFS[k];
        return '<div class="schema-group"><h3>' + def.title + "</h3>" + def.tables.map(schemaTableRow).join("") + "</div>";
      }).join("") +
    "</div>" +
  "</div>";
}

function wireSchemaReference() {
  var toggle = document.getElementById("schemaRefToggle");
  var body = document.getElementById("schemaRefBody");
  if (!toggle || !body) return;
  toggle.addEventListener("click", function () {
    body.hidden = !body.hidden;
    toggle.textContent = body.hidden ? "📋 テーブル構成（列一覧）を見る ▾" : "🙈 テーブル構成を隠す ▴";
  });
}

function renderPracticeArena(problems, containers) {
  var intro = document.querySelector(".arena-intro");
  if (intro && !document.getElementById("schemaRef")) {
    intro.insertAdjacentHTML("afterend", buildSchemaRefHTML());
    wireSchemaReference();
  }
  var byTier = { basic: containers.basicsEl, intermediate: containers.intermediateEl, advanced: containers.advancedEl };
  problems.forEach(function (p) {
    var target = byTier[p.tier];
    if (!target) return;
    var card = buildPracticeCard(p);
    target.appendChild(card);
  });
  problems.forEach(wirePracticeCard);

  SQL_ENGINE.init().then(function () {
    document.querySelectorAll(".sql-engine-status").forEach(function (el) {
      el.textContent = "✅ SQLエンジンの準備ができました。実際にクエリを実行できます。";
      el.className = "sql-engine-status ready";
    });
  }).catch(function (err) {
    document.querySelectorAll(".sql-engine-status").forEach(function (el) {
      el.textContent = "⚠️ SQLエンジンの読み込みに失敗しました。インターネット接続を確認して再読み込みしてください。";
      el.className = "sql-engine-status error";
    });
  });
}
