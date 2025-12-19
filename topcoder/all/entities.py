from dataclasses import dataclass
from typing import Optional
import json


@dataclass
class Round_propertie:
    string_value: Optional[str]
    int_value: int
    round_id: int
    property_name: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Round_propertie':
        return cls(
            string_value=data.get('string_value'),
            int_value=int(data.get('int_value', '0')) if data.get('int_value') else 0,
            round_id=int(data.get('round_id', '0')) if data.get('round_id') else 0,
            property_name=data.get('property_name')
        )


@dataclass
class Round_component:
    default_solution: Optional[str]
    component_type_id: int
    problem_id: int
    method_name: str
    open_order: int
    round_id: int
    submit_order: int
    result_type_id: int
    class_name: str
    component_id: int
    division_id: int
    status_id: int
    modify_date: Optional[str]
    difficulty_id: int
    points: float
    component_text: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Round_component':
        return cls(
            default_solution=data.get('default_solution'),
            component_type_id=int(data.get('component_type_id', '0')) if data.get('component_type_id') else 0,
            problem_id=int(data.get('problem_id', '0')) if data.get('problem_id') else 0,
            method_name=data.get('method_name'),
            open_order=int(data.get('open_order', '0')) if data.get('open_order') else 0,
            round_id=int(data.get('round_id', '0')) if data.get('round_id') else 0,
            submit_order=int(data.get('submit_order', '0')) if data.get('submit_order') else 0,
            result_type_id=int(data.get('result_type_id', '0')) if data.get('result_type_id') else 0,
            class_name=data.get('class_name'),
            component_id=int(data.get('component_id', '0')) if data.get('component_id') else 0,
            division_id=int(data.get('division_id', '0')) if data.get('division_id') else 0,
            status_id=int(data.get('status_id', '0')) if data.get('status_id') else 0,
            modify_date=data.get('modify_date'),
            difficulty_id=int(data.get('difficulty_id', '0')) if data.get('difficulty_id') else 0,
            points=float(data.get('points', '0.0')) if data.get('points') else 0.0,
            component_text=data.get('component_text')
        )


@dataclass
class Problem_rating:
    problem_id: int
    create_date: str
    problem_rating: int
    question_id: int
    modify_date: Optional[str]
    coder_id: int

    @classmethod
    def from_dict(cls, data: dict) -> 'Problem_rating':
        return cls(
            problem_id=int(data.get('problem_id', '0')) if data.get('problem_id') else 0,
            create_date=data.get('create_date'),
            problem_rating=int(data.get('problem_rating', '0')) if data.get('problem_rating') else 0,
            question_id=int(data.get('question_id', '0')) if data.get('question_id') else 0,
            modify_date=data.get('modify_date'),
            coder_id=int(data.get('coder_id', '0')) if data.get('coder_id') else 0
        )


@dataclass
class Room_result:
    point_total: float
    team_points: Optional[str]
    new_vol: Optional[str]
    attended: Optional[str]
    old_vol: Optional[str]
    region_placed: Optional[str]
    room_placed: Optional[str]
    room_seed: Optional[str]
    advanced: str
    division_placed: Optional[str]
    rated_flag: Optional[str]
    division_seed: Optional[str]
    overall_rank: Optional[str]
    new_rating: Optional[str]
    round_payment_id: Optional[str]
    room_id: int
    paid: Optional[str]
    round_id: int
    old_rating: Optional[str]
    coder_id: int

    @classmethod
    def from_dict(cls, data: dict) -> 'Room_result':
        return cls(
            point_total=float(data.get('point_total', '0.0')) if data.get('point_total') else 0.0,
            team_points=data.get('team_points'),
            new_vol=data.get('new_vol'),
            attended=data.get('attended'),
            old_vol=data.get('old_vol'),
            region_placed=data.get('region_placed'),
            room_placed=data.get('room_placed'),
            room_seed=data.get('room_seed'),
            advanced=data.get('advanced'),
            division_placed=data.get('division_placed'),
            rated_flag=data.get('rated_flag'),
            division_seed=data.get('division_seed'),
            overall_rank=data.get('overall_rank'),
            new_rating=data.get('new_rating'),
            round_payment_id=data.get('round_payment_id'),
            room_id=int(data.get('room_id', '0')) if data.get('room_id') else 0,
            paid=data.get('paid'),
            round_id=int(data.get('round_id', '0')) if data.get('round_id') else 0,
            old_rating=data.get('old_rating'),
            coder_id=int(data.get('coder_id', '0')) if data.get('coder_id') else 0
        )


@dataclass
class Round_segment:
    status: str
    segment_desc: str
    round_id: int
    start_time: str
    end_time: str
    segment_id: int

    @classmethod
    def from_dict(cls, data: dict) -> 'Round_segment':
        return cls(
            status=data.get('status'),
            segment_desc=data.get('segment_desc'),
            round_id=int(data.get('round_id', '0')) if data.get('round_id') else 0,
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            segment_id=int(data.get('segment_id', '0')) if data.get('segment_id') else 0
        )


@dataclass
class Round_registration:
    eligible: int
    timestamp: str
    round_id: int
    team_id: Optional[str]
    coder_id: int

    @classmethod
    def from_dict(cls, data: dict) -> 'Round_registration':
        return cls(
            eligible=int(data.get('eligible', '0')) if data.get('eligible') else 0,
            timestamp=data.get('timestamp'),
            round_id=int(data.get('round_id', '0')) if data.get('round_id') else 0,
            team_id=data.get('team_id'),
            coder_id=int(data.get('coder_id', '0')) if data.get('coder_id') else 0
        )


@dataclass
class Difficultie:
    difficulty_desc: str
    difficulty_level: str
    difficulty_id: int
    point_value: int

    @classmethod
    def from_dict(cls, data: dict) -> 'Difficultie':
        return cls(
            difficulty_desc=data.get('difficulty_desc'),
            difficulty_level=data.get('difficulty_level'),
            difficulty_id=int(data.get('difficulty_id', '0')) if data.get('difficulty_id') else 0,
            point_value=int(data.get('point_value', '0')) if data.get('point_value') else 0
        )


@dataclass
class Component_category:
    component_category_id: int
    component_id: int
    component_category_desc: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Component_category':
        return cls(
            component_category_id=int(data.get('component_category_id', '0')) if data.get('component_category_id') else 0,
            component_id=int(data.get('component_id', '0')) if data.get('component_id') else 0,
            component_category_desc=data.get('component_category_desc')
        )


@dataclass
class System_test_case:
    status: Optional[str]
    example_flag: Optional[str]
    args: str
    system_flag: int
    test_case_id: int
    modify_date: str
    component_id: int
    test_number: Optional[str]
    expected_result: str

    @classmethod
    def from_dict(cls, data: dict) -> 'System_test_case':
        return cls(
            status=data.get('status'),
            example_flag=data.get('example_flag'),
            args=data.get('args'),
            system_flag=int(data.get('system_flag', '0')) if data.get('system_flag') else 0,
            test_case_id=int(data.get('test_case_id', '0')) if data.get('test_case_id') else 0,
            modify_date=data.get('modify_date'),
            component_id=int(data.get('component_id', '0')) if data.get('component_id') else 0,
            test_number=data.get('test_number'),
            expected_result=data.get('expected_result')
        )


@dataclass
class Solution_history:
    user_id: int
    modify_date: str
    solution: str
    solution_id: int

    @classmethod
    def from_dict(cls, data: dict) -> 'Solution_history':
        return cls(
            user_id=int(data.get('user_id', '0')) if data.get('user_id') else 0,
            modify_date=data.get('modify_date'),
            solution=data.get('solution'),
            solution_id=int(data.get('solution_id', '0')) if data.get('solution_id') else 0
        )


@dataclass
class Contest:
    region_code: Optional[str]
    status: str
    season_id: Optional[str]
    contest_id: int
    end_date: Optional[str]
    group_id: int
    ad_command: Optional[str]
    name: str
    ad_task: Optional[str]
    ad_text: Optional[str]
    ad_start: Optional[str]
    language_id: Optional[str]
    start_date: Optional[str]
    ad_end: Optional[str]
    activate_menu: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> 'Contest':
        return cls(
            region_code=data.get('region_code'),
            status=data.get('status'),
            season_id=data.get('season_id'),
            contest_id=int(data.get('contest_id', '0')) if data.get('contest_id') else 0,
            end_date=data.get('end_date'),
            group_id=int(data.get('group_id', '0')) if data.get('group_id') else 0,
            ad_command=data.get('ad_command'),
            name=data.get('name'),
            ad_task=data.get('ad_task'),
            ad_text=data.get('ad_text'),
            ad_start=data.get('ad_start'),
            language_id=data.get('language_id'),
            start_date=data.get('start_date'),
            ad_end=data.get('ad_end'),
            activate_menu=data.get('activate_menu')
        )


@dataclass
class Round_room_assignment:
    p: float
    by_division: int
    round_id: int
    algorithm: int
    by_region: int
    final: int
    coders_per_room: int

    @classmethod
    def from_dict(cls, data: dict) -> 'Round_room_assignment':
        return cls(
            p=float(data.get('p', '0.0')) if data.get('p') else 0.0,
            by_division=int(data.get('by_division', '0')) if data.get('by_division') else 0,
            round_id=int(data.get('round_id', '0')) if data.get('round_id') else 0,
            algorithm=int(data.get('algorithm', '0')) if data.get('algorithm') else 0,
            by_region=int(data.get('by_region', '0')) if data.get('by_region') else 0,
            final=int(data.get('final', '0')) if data.get('final') else 0,
            coders_per_room=int(data.get('coders_per_room', '0')) if data.get('coders_per_room') else 0
        )


@dataclass
class Component_state:
    submission_number: int
    system_test_version: int
    component_state_id: int
    round_id: int
    component_id: int
    status_id: int
    coder_id: int
    language_id: Optional[str]
    points: float

    @classmethod
    def from_dict(cls, data: dict) -> 'Component_state':
        return cls(
            submission_number=int(data.get('submission_number', '0')) if data.get('submission_number') else 0,
            system_test_version=int(data.get('system_test_version', '0')) if data.get('system_test_version') else 0,
            component_state_id=int(data.get('component_state_id', '0')) if data.get('component_state_id') else 0,
            round_id=int(data.get('round_id', '0')) if data.get('round_id') else 0,
            component_id=int(data.get('component_id', '0')) if data.get('component_id') else 0,
            status_id=int(data.get('status_id', '0')) if data.get('status_id') else 0,
            coder_id=int(data.get('coder_id', '0')) if data.get('coder_id') else 0,
            language_id=data.get('language_id'),
            points=float(data.get('points', '0.0')) if data.get('points') else 0.0
        )


@dataclass
class Compilation:
    component_state_id: int
    compilation_text: str
    compilation_class_file: Optional[str]
    language_id: Optional[str]
    open_time: int

    @classmethod
    def from_dict(cls, data: dict) -> 'Compilation':
        return cls(
            component_state_id=int(data.get('component_state_id', '0')) if data.get('component_state_id') else 0,
            compilation_text=data.get('compilation_text'),
            compilation_class_file=data.get('compilation_class_file'),
            language_id=data.get('language_id'),
            open_time=int(data.get('open_time', '0')) if data.get('open_time') else 0
        )


@dataclass
class Round:
    rated_ind: int
    status: str
    short_name: Optional[str]
    calendar_ind: int
    round_type_desc: str
    contest_id: int
    round_id: int
    invitational: Optional[str]
    language_name: Optional[str]
    name: str
    link: Optional[str]
    region_id: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> 'Round':
        return cls(
            rated_ind=int(data.get('rated_ind', '0')) if data.get('rated_ind') else 0,
            status=data.get('status'),
            short_name=data.get('short_name'),
            calendar_ind=int(data.get('calendar_ind', '0')) if data.get('calendar_ind') else 0,
            round_type_desc=data.get('round_type_desc'),
            contest_id=int(data.get('contest_id', '0')) if data.get('contest_id') else 0,
            round_id=int(data.get('round_id', '0')) if data.get('round_id') else 0,
            invitational=data.get('invitational'),
            language_name=data.get('language_name'),
            name=data.get('name'),
            link=data.get('link'),
            region_id=data.get('region_id')
        )


@dataclass
class User:
    handle: str
    user_id: int

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        return cls(
            handle=data.get('handle'),
            user_id=int(data.get('user_id', '0')) if data.get('user_id') else 0
        )


@dataclass
class System_test_output:
    stdout: Optional[str]
    round_id: int
    test_case_id: int
    stderr: Optional[str]
    component_id: int
    coder_id: int

    @classmethod
    def from_dict(cls, data: dict) -> 'System_test_output':
        return cls(
            stdout=data.get('stdout'),
            round_id=int(data.get('round_id', '0')) if data.get('round_id') else 0,
            test_case_id=int(data.get('test_case_id', '0')) if data.get('test_case_id') else 0,
            stderr=data.get('stderr'),
            component_id=int(data.get('component_id', '0')) if data.get('component_id') else 0,
            coder_id=int(data.get('coder_id', '0')) if data.get('coder_id') else 0
        )


@dataclass
class Component_status_lu:
    component_status_id: int
    status_desc: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Component_status_lu':
        return cls(
            component_status_id=int(data.get('component_status_id', '0')) if data.get('component_status_id') else 0,
            status_desc=data.get('status_desc')
        )


@dataclass
class Solution:
    package: str
    has_check_answer: bool
    primary_solution: Optional[str]
    component_id: Optional[str]
    solution_text: str
    coder_id: int
    modify_date: str
    language_id: int
    solution_id: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> 'Solution':
        return cls(
            package=data.get('package'),
            has_check_answer=data.get('has_check_answer'),
            primary_solution=data.get('primary_solution'),
            component_id=data.get('component_id'),
            solution_text=data.get('solution_text'),
            coder_id=int(data.get('coder_id', '0')) if data.get('coder_id') else 0,
            modify_date=data.get('modify_date'),
            language_id=int(data.get('language_id', '0')) if data.get('language_id') else 0,
            solution_id=data.get('solution_id')
        )


@dataclass
class Problem:
    problem_id: int
    proposed_difficulty_id: int
    create_date: str
    problem_text: Optional[str]
    name: str
    accept_submissions: int
    modify_date: str
    status_id: int
    proposed_division_id: int
    problem_type_id: int

    @classmethod
    def from_dict(cls, data: dict) -> 'Problem':
        return cls(
            problem_id=int(data.get('problem_id', '0')) if data.get('problem_id') else 0,
            proposed_difficulty_id=int(data.get('proposed_difficulty_id', '0')) if data.get('proposed_difficulty_id') else 0,
            create_date=data.get('create_date'),
            problem_text=data.get('problem_text'),
            name=data.get('name'),
            accept_submissions=int(data.get('accept_submissions', '0')) if data.get('accept_submissions') else 0,
            modify_date=data.get('modify_date'),
            status_id=int(data.get('status_id', '0')) if data.get('status_id') else 0,
            proposed_division_id=int(data.get('proposed_division_id', '0')) if data.get('proposed_division_id') else 0,
            problem_type_id=int(data.get('problem_type_id', '0')) if data.get('problem_type_id') else 0
        )


@dataclass
class Round_event:
    event_name: str
    registration_url: str
    event_id: int
    start_registration: str
    end_registration: str
    round_id: int
    terms_of_use_id: int
    event_type_id: int
    event_desc: str
    modify_date: str
    survey_id: Optional[str]
    event_short_desc: str
    parent_event_id: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> 'Round_event':
        return cls(
            event_name=data.get('event_name'),
            registration_url=data.get('registration_url'),
            event_id=int(data.get('event_id', '0')) if data.get('event_id') else 0,
            start_registration=data.get('start_registration'),
            end_registration=data.get('end_registration'),
            round_id=int(data.get('round_id', '0')) if data.get('round_id') else 0,
            terms_of_use_id=int(data.get('terms_of_use_id', '0')) if data.get('terms_of_use_id') else 0,
            event_type_id=int(data.get('event_type_id', '0')) if data.get('event_type_id') else 0,
            event_desc=data.get('event_desc'),
            modify_date=data.get('modify_date'),
            survey_id=data.get('survey_id'),
            event_short_desc=data.get('event_short_desc'),
            parent_event_id=data.get('parent_event_id')
        )


@dataclass
class Problem_payment:
    coder_id: int
    problem_id: int
    pending: float
    paid: float

    @classmethod
    def from_dict(cls, data: dict) -> 'Problem_payment':
        return cls(
            coder_id=int(data.get('coder_id', '0')) if data.get('coder_id') else 0,
            problem_id=int(data.get('problem_id', '0')) if data.get('problem_id') else 0,
            pending=float(data.get('pending', '0.0')) if data.get('pending') else 0.0,
            paid=float(data.get('paid', '0.0')) if data.get('paid') else 0.0
        )


@dataclass
class Room:
    region_code: Optional[str]
    eligible: Optional[str]
    room_type_id: int
    round_id: int
    room_limit: Optional[str]
    unrated: Optional[str]
    name: str
    division_id: int
    room_type_desc: str
    country_code: Optional[str]
    room_id: int
    state_code: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> 'Room':
        return cls(
            region_code=data.get('region_code'),
            eligible=data.get('eligible'),
            room_type_id=int(data.get('room_type_id', '0')) if data.get('room_type_id') else 0,
            round_id=int(data.get('round_id', '0')) if data.get('round_id') else 0,
            room_limit=data.get('room_limit'),
            unrated=data.get('unrated'),
            name=data.get('name'),
            division_id=int(data.get('division_id', '0')) if data.get('division_id') else 0,
            room_type_desc=data.get('room_type_desc'),
            country_code=data.get('country_code'),
            room_id=int(data.get('room_id', '0')) if data.get('room_id') else 0,
            state_code=data.get('state_code')
        )


@dataclass
class Challenge:
    args: str
    defendant_id: int
    succeeded: int
    round_id: int
    received: str
    message: str
    challenge_id: int
    challenger_id: int
    expected: str
    challenger_points: float
    component_id: int
    status_id: int
    defendant_points: float
    check_answer_response: Optional[str]
    submit_time: int

    @classmethod
    def from_dict(cls, data: dict) -> 'Challenge':
        return cls(
            args=data.get('args'),
            defendant_id=int(data.get('defendant_id', '0')) if data.get('defendant_id') else 0,
            succeeded=int(data.get('succeeded', '0')) if data.get('succeeded') else 0,
            round_id=int(data.get('round_id', '0')) if data.get('round_id') else 0,
            received=data.get('received'),
            message=data.get('message'),
            challenge_id=int(data.get('challenge_id', '0')) if data.get('challenge_id') else 0,
            challenger_id=int(data.get('challenger_id', '0')) if data.get('challenger_id') else 0,
            expected=data.get('expected'),
            challenger_points=float(data.get('challenger_points', '0.0')) if data.get('challenger_points') else 0.0,
            component_id=int(data.get('component_id', '0')) if data.get('component_id') else 0,
            status_id=int(data.get('status_id', '0')) if data.get('status_id') else 0,
            defendant_points=float(data.get('defendant_points', '0.0')) if data.get('defendant_points') else 0.0,
            check_answer_response=data.get('check_answer_response'),
            submit_time=int(data.get('submit_time', '0')) if data.get('submit_time') else 0
        )