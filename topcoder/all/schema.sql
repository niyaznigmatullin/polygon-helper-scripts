CREATE TABLE round_properties (
    string_value TEXT,
    int_value TEXT,
    round_id TEXT,
    property_name TEXT
);

CREATE TABLE round_component (
    default_solution TEXT,
    component_type_id TEXT,
    problem_id TEXT,
    method_name TEXT,
    open_order TEXT,
    round_id TEXT,
    submit_order TEXT,
    result_type_id TEXT,
    class_name TEXT,
    component_id TEXT,
    division_id TEXT,
    status_id TEXT,
    modify_date TEXT,
    difficulty_id TEXT,
    points TEXT,
    component_text TEXT
);

CREATE TABLE problem_ratings (
    problem_id TEXT,
    create_date TEXT,
    problem_rating TEXT,
    question_id TEXT,
    modify_date TEXT,
    coder_id TEXT
);

CREATE TABLE room_results (
    point_total TEXT,
    team_points TEXT,
    new_vol TEXT,
    attended TEXT,
    old_vol TEXT,
    region_placed TEXT,
    room_placed TEXT,
    room_seed TEXT,
    advanced TEXT,
    division_placed TEXT,
    rated_flag TEXT,
    division_seed TEXT,
    overall_rank TEXT,
    new_rating TEXT,
    round_payment_id TEXT,
    room_id TEXT,
    paid TEXT,
    round_id TEXT,
    old_rating TEXT,
    coder_id TEXT
);

CREATE TABLE round_segments (
    status TEXT,
    segment_desc TEXT,
    round_id TEXT,
    start_time TEXT,
    end_time TEXT,
    segment_id TEXT
);

CREATE TABLE round_registrations (
    eligible TEXT,
    timestamp TEXT,
    round_id TEXT,
    team_id TEXT,
    coder_id TEXT
);

CREATE TABLE difficulties (
    difficulty_desc TEXT,
    difficulty_level TEXT,
    difficulty_id TEXT,
    point_value TEXT
);

CREATE TABLE component_category (
    component_category_id TEXT,
    component_id TEXT,
    component_category_desc TEXT
);

CREATE TABLE system_test_cases (
    status TEXT,
    example_flag TEXT,
    args TEXT,
    system_flag TEXT,
    test_case_id TEXT,
    modify_date TEXT,
    component_id TEXT,
    test_number TEXT,
    expected_result TEXT
);

CREATE TABLE solution_history (
    user_id TEXT,
    modify_date TEXT,
    solution TEXT,
    solution_id TEXT
);

CREATE TABLE contest (
    region_code TEXT,
    status TEXT,
    season_id TEXT,
    contest_id TEXT,
    end_date TEXT,
    group_id TEXT,
    ad_command TEXT,
    name TEXT,
    ad_task TEXT,
    ad_text TEXT,
    ad_start TEXT,
    language_id TEXT,
    start_date TEXT,
    ad_end TEXT,
    activate_menu TEXT
);

CREATE TABLE round_room_assignments (
    p TEXT,
    by_division TEXT,
    round_id TEXT,
    algorithm TEXT,
    by_region TEXT,
    final TEXT,
    coders_per_room TEXT
);

CREATE TABLE component_state (
    submission_number TEXT,
    system_test_version TEXT,
    component_state_id TEXT,
    round_id TEXT,
    component_id TEXT,
    status_id TEXT,
    coder_id TEXT,
    language_id TEXT,
    points TEXT
);

CREATE TABLE compilation (
    component_state_id TEXT,
    compilation_text TEXT,
    compilation_class_file TEXT,
    language_id TEXT,
    open_time TEXT
);

CREATE TABLE rounds (
    rated_ind TEXT,
    status TEXT,
    short_name TEXT,
    calendar_ind TEXT,
    round_type_desc TEXT,
    contest_id TEXT,
    round_id TEXT,
    invitational TEXT,
    language_name TEXT,
    name TEXT,
    link TEXT,
    region_id TEXT
);

CREATE TABLE users (
    handle TEXT,
    user_id TEXT
);

CREATE TABLE system_test_output (
    stdout TEXT,
    round_id TEXT,
    test_case_id TEXT,
    stderr TEXT,
    component_id TEXT,
    coder_id TEXT
);

CREATE TABLE component_status_lu (
    component_status_id TEXT,
    status_desc TEXT
);

CREATE TABLE solutions (
    package TEXT,
    has_check_answer INTEGER,
    primary_solution TEXT,
    component_id TEXT,
    solution_text TEXT,
    coder_id TEXT,
    modify_date TEXT,
    language_id TEXT,
    solution_id TEXT
);

CREATE TABLE problems (
    problem_id TEXT,
    proposed_difficulty_id TEXT,
    create_date TEXT,
    problem_text TEXT,
    name TEXT,
    accept_submissions TEXT,
    modify_date TEXT,
    status_id TEXT,
    proposed_division_id TEXT,
    problem_type_id TEXT
);

CREATE TABLE round_events (
    event_name TEXT,
    registration_url TEXT,
    event_id TEXT,
    start_registration TEXT,
    end_registration TEXT,
    round_id TEXT,
    terms_of_use_id TEXT,
    event_type_id TEXT,
    event_desc TEXT,
    modify_date TEXT,
    survey_id TEXT,
    event_short_desc TEXT,
    parent_event_id TEXT
);

CREATE TABLE problem_payments (
    coder_id TEXT,
    problem_id TEXT,
    pending TEXT,
    paid TEXT
);

CREATE TABLE rooms (
    region_code TEXT,
    eligible TEXT,
    room_type_id TEXT,
    round_id TEXT,
    room_limit TEXT,
    unrated TEXT,
    name TEXT,
    division_id TEXT,
    room_type_desc TEXT,
    country_code TEXT,
    room_id TEXT,
    state_code TEXT
);

CREATE TABLE challenges (
    args TEXT,
    defendant_id TEXT,
    succeeded TEXT,
    round_id TEXT,
    received TEXT,
    message TEXT,
    challenge_id TEXT,
    challenger_id TEXT,
    expected TEXT,
    challenger_points TEXT,
    component_id TEXT,
    status_id TEXT,
    defendant_points TEXT,
    check_answer_response TEXT,
    submit_time TEXT
);