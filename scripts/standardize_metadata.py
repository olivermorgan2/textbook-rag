#!/usr/bin/env python3
"""Standardize all chapter metadata JSON files to a unified schema."""

import json
import os
import re
import copy

CHAPTERS_DIR = os.path.join(os.path.dirname(__file__), '..', 'textbook', 'chapters')

# Bloom's taxonomy mapping: old -> revised
BLOOM_MAP = {
    'knowledge': 'Remember',
    'remember': 'Remember',
    'comprehension': 'Understand',
    'understand': 'Understand',
    'understanding': 'Understand',
    'application': 'Apply',
    'apply': 'Apply',
    'analysis': 'Analyze',
    'analyze': 'Analyze',
    'synthesis': 'Create',
    'synthesize': 'Create',
    'create': 'Create',
    'creation': 'Create',
    'design': 'Create',
    'evaluation': 'Evaluate',
    'evaluate': 'Evaluate',
    'assess': 'Evaluate',
    'identify': 'Remember',
    'compare': 'Analyze',
    'critique': 'Evaluate',
}

# WHO region normalization
WHO_REGION_MAP = {
    'afro': 'African Region',
    'afr': 'African Region',
    'african': 'African Region',
    'african region': 'African Region',
    'africa': 'African Region',
    'who african region': 'African Region',
    'amro': 'Region of the Americas',
    'amr': 'Region of the Americas',
    'paho': 'Region of the Americas',
    'paho/amro': 'Region of the Americas',
    'americas': 'Region of the Americas',
    'americas region': 'Region of the Americas',
    'region of the americas': 'Region of the Americas',
    'who region of the americas': 'Region of the Americas',
    'searo': 'South-East Asia Region',
    'sear': 'South-East Asia Region',
    'south-east asia': 'South-East Asia Region',
    'south-east asia region': 'South-East Asia Region',
    'southeast asia': 'South-East Asia Region',
    'who south-east asia region': 'South-East Asia Region',
    'euro': 'European Region',
    'eur': 'European Region',
    'european': 'European Region',
    'european region': 'European Region',
    'who european region': 'European Region',
    'emro': 'Eastern Mediterranean Region',
    'emr': 'Eastern Mediterranean Region',
    'eastern mediterranean': 'Eastern Mediterranean Region',
    'eastern mediterranean region': 'Eastern Mediterranean Region',
    'who eastern mediterranean region': 'Eastern Mediterranean Region',
    'wpro': 'Western Pacific Region',
    'wpr': 'Western Pacific Region',
    'western pacific': 'Western Pacific Region',
    'western pacific region': 'Western Pacific Region',
    'who western pacific region': 'Western Pacific Region',
}

# Part number mapping
ROMAN_TO_INT = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10}

# Known part titles by number
PART_TITLES = {
    1: 'Foundations of Global Public Health',
    2: 'Communicable Diseases',
    3: 'Non-Communicable Diseases',
    4: 'Special Populations and Life Course Approach',
    5: 'Environmental and Social Determinants',
    6: 'Global Health Interventions and Programs',
    7: 'Policy, Governance, and Future Directions',
}


def normalize_bloom(level):
    """Normalize a Bloom's taxonomy level to the revised version."""
    if not level:
        return None
    return BLOOM_MAP.get(level.lower().strip(), level.strip())


def normalize_who_region(region_str):
    """Normalize a WHO region string to standard form."""
    if not region_str:
        return None
    # Strip parenthetical country info like "African Region (Ghana, South Africa)"
    clean = re.sub(r'\s*\(.*?\)', '', region_str).strip()
    # Remove "WHO " prefix
    clean = re.sub(r'^WHO\s+', '', clean, flags=re.IGNORECASE)
    key = clean.lower().strip()
    if key in WHO_REGION_MAP:
        return WHO_REGION_MAP[key]
    # Try matching just the first word(s)
    for k, v in WHO_REGION_MAP.items():
        if key.startswith(k):
            return v
    # If it contains a known region name, extract it
    for k, v in WHO_REGION_MAP.items():
        if k in key:
            return v
    return region_str  # Return original if no match


def parse_part(data):
    """Extract part_number (int) and part_title (str) from various formats."""
    part_number = None
    part_title = None

    # Check for part_number directly
    if 'part_number' in data:
        pn = data['part_number']
        if isinstance(pn, int):
            part_number = pn
        elif isinstance(pn, str) and pn in ROMAN_TO_INT:
            part_number = ROMAN_TO_INT[pn]

    # Check for part_title directly
    if 'part_title' in data:
        part_title = data['part_title']

    # Check chapter wrapper for part_number/part_title
    for wrapper_key in ['chapter', 'chapter_info', 'chapter_metadata']:
        wrapper = data.get(wrapper_key, {})
        if isinstance(wrapper, dict):
            if 'part_number' in wrapper and part_number is None:
                pn = wrapper['part_number']
                if isinstance(pn, int):
                    part_number = pn
            if 'part_title' in wrapper and part_title is None:
                part_title = wrapper['part_title']

    # Now handle the 'part' field
    part_val = None
    for source in [data] + [data.get(k, {}) for k in ['chapter', 'chapter_info', 'chapter_metadata'] if isinstance(data.get(k), dict)]:
        if isinstance(source, dict) and 'part' in source:
            part_val = source['part']
            # Also grab part_title from same level if present
            if 'part_title' in source and part_title is None:
                part_title = source['part_title']
            break

    if part_val is not None:
        if isinstance(part_val, dict):
            # {"number": 2, "title": "Communicable Diseases"}
            part_number = part_val.get('number') or part_val.get('part_number', part_number)
            part_title = part_val.get('title') or part_val.get('part_title', part_title)
        elif isinstance(part_val, int):
            part_number = part_val
        elif isinstance(part_val, str):
            # "Part I: Foundations of Global Public Health"
            m = re.match(r'Part\s+([IVXLC]+)\s*:\s*(.*)', part_val)
            if m:
                roman = m.group(1).strip()
                part_number = ROMAN_TO_INT.get(roman, part_number)
                part_title = m.group(2).strip() or part_title
            elif part_val.strip() in ROMAN_TO_INT:
                # Just "III"
                part_number = ROMAN_TO_INT[part_val.strip()]
            else:
                # "IV: Special Populations..."
                m2 = re.match(r'([IVXLC]+)\s*:\s*(.*)', part_val)
                if m2:
                    part_number = ROMAN_TO_INT.get(m2.group(1).strip(), part_number)
                    part_title = m2.group(2).strip() or part_title
                elif part_val.strip() in ROMAN_TO_INT:
                    part_number = ROMAN_TO_INT[part_val.strip()]

    # Fill in part_title from known mapping if we have a number but no title
    if part_number and not part_title:
        part_title = PART_TITLES.get(part_number, None)

    if part_number is not None:
        return {"part_number": part_number, "part_title": part_title}
    return None


def extract_chapter_info(data):
    """Extract chapter_number and title from any wrapper structure."""
    chapter_number = None
    title = None

    # Try direct top-level
    if isinstance(data.get('chapter_number'), int):
        chapter_number = data['chapter_number']
    if isinstance(data.get('title'), str):
        title = data['title']
    if isinstance(data.get('chapter_title'), str):
        title = data['chapter_title']

    # If 'chapter' is an int (ch 15, 20)
    if isinstance(data.get('chapter'), int):
        chapter_number = data['chapter']

    # Try wrappers
    for key in ['chapter', 'chapter_info', 'chapter_metadata']:
        wrapper = data.get(key)
        if isinstance(wrapper, dict):
            if chapter_number is None:
                chapter_number = wrapper.get('chapter_number') or wrapper.get('number')
            if title is None:
                title = wrapper.get('title') or wrapper.get('chapter_title')

    return chapter_number, title


def get_wrapper(data):
    """Get the chapter info wrapper dict, or data itself for flat."""
    for key in ['chapter', 'chapter_info', 'chapter_metadata']:
        if isinstance(data.get(key), dict):
            return data[key]
    return data


def parse_word_count_target(data):
    """Extract word_count_target as {min, max}."""
    wrapper = get_wrapper(data)
    # Look for any word count field
    for key in ['word_count_target', 'estimated_length', 'word_count', 'estimated_word_count']:
        val = wrapper.get(key) or data.get(key)
        if val is not None:
            return _parse_range(val)
    return None


def _parse_range(val):
    """Parse a range value into {min, max}."""
    if isinstance(val, dict):
        mn = val.get('minimum') or val.get('min')
        mx = val.get('maximum') or val.get('max')
        if mn is not None and mx is not None:
            return {"min": int(mn), "max": int(mx)}
    if isinstance(val, int):
        return {"min": val, "max": val}
    if isinstance(val, str):
        # "7,500 words" -> 7500
        clean = re.sub(r'[,\s]*(words|word)', '', val).strip()
        m = re.match(r'(\d+)\s*[-–]\s*(\d+)', clean)
        if m:
            return {"min": int(m.group(1)), "max": int(m.group(2))}
        m2 = re.match(r'(\d+)', clean)
        if m2:
            n = int(m2.group(1))
            return {"min": n, "max": n}
    return None


def parse_reference_count_target(data):
    """Extract reference_count_target as {min, max}."""
    wrapper = get_wrapper(data)
    for key in ['reference_count_target', 'reference_target', 'citation_count_target',
                'citation_target', 'citations_target', 'primary_sources_target',
                'target_references', 'key_references_count']:
        val = wrapper.get(key) or data.get(key)
        if val is not None:
            return _parse_range_or_ref(val)
    # Check citation_target inside wrapper
    ct = wrapper.get('citation_target')
    if isinstance(ct, dict):
        mn = ct.get('minimum')
        mx = ct.get('maximum')
        if mn is not None and mx is not None:
            return {"min": int(mn), "max": int(mx)}
    return None


def _parse_range_or_ref(val):
    """Parse a reference count target value."""
    if isinstance(val, dict):
        mn = val.get('minimum') or val.get('target_minimum') or val.get('min')
        mx = val.get('maximum') or val.get('target_maximum') or val.get('max')
        if mn is not None and mx is not None:
            return {"min": int(mn), "max": int(mx)}
    if isinstance(val, int):
        return {"min": val, "max": val}
    if isinstance(val, str):
        # "40-60 primary sources" or "45-55 primary sources" or "40-60"
        m = re.search(r'(\d+)\s*[-–]\s*(\d+)', val)
        if m:
            return {"min": int(m.group(1)), "max": int(m.group(2))}
        m2 = re.match(r'(\d+)', val)
        if m2:
            n = int(m2.group(1))
            return {"min": n, "max": n}
    return None


def normalize_learning_objectives(data):
    """Normalize learning objectives to a flat array with bloom_level on each."""
    objectives = []

    # Find the learning_objectives field
    lo = data.get('learning_objectives')
    if lo is None:
        wrapper = get_wrapper(data)
        lo = wrapper.get('learning_objectives') if isinstance(wrapper, dict) else None

    if lo is None:
        return objectives

    if isinstance(lo, list):
        # Already a flat array of objects
        for obj in lo:
            objectives.append(_normalize_single_objective(obj))
    elif isinstance(lo, dict):
        # Check for primary/secondary split (ch 12)
        if 'primary_objectives' in lo or 'secondary_objectives' in lo:
            for obj in lo.get('primary_objectives', []):
                objectives.append(_normalize_single_objective(obj))
            for obj in lo.get('secondary_objectives', []):
                objectives.append(_normalize_single_objective(obj))
        # Check for cognitive wrapper (ch 15, 20)
        elif 'cognitive' in lo or 'cognitive_levels' in lo:
            inner = lo.get('cognitive') or lo.get('cognitive_levels')
            if isinstance(inner, dict):
                objectives = _flatten_bloom_keyed_objectives(inner)
        else:
            # Bloom level keys (knowledge, comprehension, etc.)
            bloom_keys = {'knowledge', 'comprehension', 'application', 'analysis', 'synthesis',
                          'evaluation', 'remember', 'understand', 'apply', 'analyze', 'evaluate', 'create'}
            if any(k.lower() in bloom_keys for k in lo.keys()):
                objectives = _flatten_bloom_keyed_objectives(lo)
            else:
                # Unknown dict structure, try to flatten
                for key, val in lo.items():
                    if isinstance(val, list):
                        for item in val:
                            if isinstance(item, dict):
                                objectives.append(_normalize_single_objective(item))
                            elif isinstance(item, str):
                                objectives.append({
                                    "bloom_level": normalize_bloom(key),
                                    "text": item
                                })

    return objectives


def _flatten_bloom_keyed_objectives(bloom_dict):
    """Flatten a dict keyed by Bloom levels into a flat list."""
    objectives = []
    for bloom_key, items in bloom_dict.items():
        bloom_level = normalize_bloom(bloom_key)
        if isinstance(items, list):
            for item in items:
                if isinstance(item, str):
                    objectives.append({
                        "bloom_level": bloom_level,
                        "text": item
                    })
                elif isinstance(item, dict):
                    obj = _normalize_single_objective(item)
                    if not obj.get('bloom_level'):
                        obj['bloom_level'] = bloom_level
                    objectives.append(obj)
    return objectives


def _normalize_single_objective(obj):
    """Normalize a single learning objective object."""
    result = {}

    # ID
    obj_id = obj.get('objective_id') or obj.get('id')
    if obj_id:
        result['objective_id'] = obj_id

    # Bloom level
    bloom = obj.get('bloom_level') or obj.get('cognitive_level') or obj.get('level') or obj.get('bloom_category') or obj.get('bloom_taxonomy')
    if bloom:
        result['bloom_level'] = normalize_bloom(bloom)

    # Text
    text = obj.get('text') or obj.get('objective')
    if text:
        result['text'] = text

    # Assessment method
    am = obj.get('assessment_method')
    if am:
        result['assessment_method'] = am

    # Assessment alignment
    aa = obj.get('assessment_alignment')
    if aa:
        result['assessment_alignment'] = aa

    # Topic area
    ta = obj.get('topic_area')
    if ta:
        result['topic_area'] = ta

    # SDG target
    sdg = obj.get('sdg_target')
    if sdg:
        result['sdg_target'] = sdg

    return result


def normalize_case_studies(data):
    """Normalize case studies to a consistent array format."""
    cs = data.get('case_studies')
    if cs is None:
        wrapper = get_wrapper(data)
        cs = wrapper.get('case_studies') if isinstance(wrapper, dict) else None

    if cs is None:
        return None

    # If it's a dict keyed by theme (ch 22), convert to array
    if isinstance(cs, dict):
        result = []
        for theme_key, study in cs.items():
            if isinstance(study, dict):
                normalized = _normalize_single_case_study(study)
                result.append(normalized)
        return result

    if isinstance(cs, list):
        return [_normalize_single_case_study(s) for s in cs if isinstance(s, dict)]

    return None


def _normalize_single_case_study(study):
    """Normalize a single case study object."""
    result = {}

    # ID
    cs_id = study.get('case_study_id') or study.get('id')
    if cs_id:
        result['case_study_id'] = cs_id

    # Title
    if 'title' in study:
        result['title'] = study['title']

    # Country/countries
    country = study.get('country')
    countries = study.get('countries')
    if country:
        result['country'] = country
    if countries:
        result['countries'] = countries

    # WHO region - normalize
    who_region = study.get('who_region') or study.get('region')
    if who_region:
        if isinstance(who_region, list):
            result['who_region'] = [normalize_who_region(r) for r in who_region]
        elif isinstance(who_region, str):
            if who_region.lower() in ('all regions', 'global', 'multiple regions', 'multiple who regions'):
                result['who_region'] = who_region
            else:
                result['who_region'] = normalize_who_region(who_region)

    # Income level
    il = study.get('income_level') or study.get('income_classification') or study.get('income_levels') or study.get('country_income')
    if il:
        result['income_level'] = il

    # Geographic focus
    gf = study.get('geographic_focus') or study.get('location')
    if gf:
        result['geographic_focus'] = gf

    # Population
    pop = study.get('population_size') or study.get('population')
    if pop:
        result['population_size'] = pop

    # Population focus
    pf = study.get('population_focus')
    if pf:
        result['population_focus'] = pf

    # Time period
    tp = study.get('time_period') or study.get('timeframe')
    if tp:
        result['time_period'] = tp

    # Focus/theme
    focus = study.get('focus') or study.get('theme')
    if focus:
        result['focus'] = focus

    # Intervention type
    it = study.get('intervention_type') or study.get('intervention')
    if it:
        if isinstance(it, str):
            result['intervention_type'] = [it]
        else:
            result['intervention_type'] = it

    # Key themes
    kt = study.get('key_themes')
    if kt:
        result['key_themes'] = kt

    # Key interventions
    ki = study.get('key_interventions')
    if ki:
        result['key_interventions'] = ki

    # Key lessons - normalize from many field names
    lessons = (study.get('key_lessons') or study.get('key_learning') or
               study.get('key_learning_points') or study.get('lessons_learned') or
               study.get('learning_points') or study.get('focus_areas') or
               study.get('learning_focus'))
    if lessons:
        if isinstance(lessons, str):
            result['key_lessons'] = [lessons]
        else:
            result['key_lessons'] = lessons

    # Outcomes
    outcomes = study.get('outcomes') or study.get('outcomes_measured') or study.get('health_outcomes')
    if outcomes:
        result['outcomes'] = outcomes

    # Key findings
    kf = study.get('key_findings')
    if kf:
        result['key_findings'] = kf

    # Challenges
    ch = study.get('challenges')
    if ch:
        result['challenges'] = ch

    # Discussion questions/points
    dq = study.get('discussion_questions') or study.get('discussion_points')
    if dq:
        result['discussion_points'] = dq

    # Key elements (ch 15)
    ke = study.get('key_elements')
    if ke:
        result['key_elements'] = ke

    # Learning objectives refs
    lo = study.get('learning_objectives')
    if lo:
        result['learning_objectives'] = lo

    # Primary references
    pr = study.get('primary_references') or study.get('primary_sources')
    if pr:
        result['primary_references'] = pr

    # SDG alignment
    sdg = study.get('sdg_alignment')
    if sdg:
        result['sdg_alignment'] = sdg

    # Type (ch 28)
    t = study.get('type')
    if t:
        result['type'] = t

    # Outcomes highlighted (ch 28)
    oh = study.get('outcomes_highlighted')
    if oh:
        result['outcomes'] = oh

    # Learning points (ch 12 style - different from key_lessons sometimes)
    lp = study.get('learning_points')
    if lp and 'key_lessons' not in result:
        result['key_lessons'] = lp

    return result


def normalize_geographic_coverage(data):
    """Normalize geographic coverage to standard structure."""
    gc = None
    for key in ['geographic_coverage', 'geographical_coverage', 'geographic_scope',
                'global_representation', 'regional_coverage']:
        gc = data.get(key)
        if gc is not None:
            break

    if gc is None:
        return None

    result = {}

    if isinstance(gc, list):
        # Array of strings (ch 3 regional_coverage)
        result['who_regions'] = [normalize_who_region(r) for r in gc]
        return result

    if isinstance(gc, dict):
        # WHO regions
        who_regions = (gc.get('who_regions') or gc.get('WHO_regions') or
                       gc.get('who_regions_represented') or gc.get('who_regions_covered'))
        if who_regions:
            if isinstance(who_regions, list):
                normalized_regions = []
                for r in who_regions:
                    if isinstance(r, str):
                        normalized_regions.append(normalize_who_region(r))
                    elif isinstance(r, dict):
                        # {region: "...", examples/focus_countries: [...]}
                        region_name = r.get('region', '')
                        normalized_regions.append(normalize_who_region(region_name))
                result['who_regions'] = normalized_regions
            elif isinstance(who_regions, dict):
                # Object keyed by region (ch 22)
                result['who_regions'] = [normalize_who_region(k) for k in who_regions.keys()]

        # Income levels
        il = (gc.get('income_levels') or gc.get('income_levels_represented') or
              gc.get('income_level_representation') or gc.get('income_classifications') or
              gc.get('income_level_coverage'))
        if il:
            if isinstance(il, list):
                result['income_levels'] = il
            elif isinstance(il, dict):
                result['income_levels'] = list(il.keys())

        # Countries
        countries = (gc.get('countries') or gc.get('specific_countries_mentioned') or
                     gc.get('specific_countries_featured') or gc.get('focus_countries'))
        if countries:
            result['countries'] = countries

        # Urban/rural
        ur = gc.get('urban_rural') or gc.get('urban_rural_contexts')
        if ur:
            result['urban_rural_contexts'] = ur

        # Regional details (ch 12 style with focus_countries per region)
        if who_regions and isinstance(who_regions, list) and len(who_regions) > 0 and isinstance(who_regions[0], dict):
            details = []
            for r in who_regions:
                detail = {"region": normalize_who_region(r.get('region', ''))}
                if 'focus_countries' in r:
                    detail['focus_countries'] = r['focus_countries']
                if 'key_topics' in r:
                    detail['focus_topics'] = r['key_topics']
                if 'examples' in r:
                    detail['examples'] = r['examples']
                details.append(detail)
            result['regional_details'] = details
            # Override who_regions with just the names
            result['who_regions'] = [d['region'] for d in details]

        # Income level detail (ch 12 style)
        if il and isinstance(il, dict):
            result['income_level_details'] = il

    return result if result else None


def normalize_assessment_materials(data):
    """Normalize assessment materials to consistent structure."""
    am = None
    for key in ['assessment_materials', 'assessment_components', 'assessment', 'assessment_methods']:
        am = data.get(key)
        if am is not None:
            break

    # Also check for review_questions (ch 20)
    rq = data.get('review_questions')

    if am is None and rq is None:
        return None

    result = {}

    if isinstance(am, dict):
        _process_assessment_dict(am, result)

    # Merge in review_questions (ch 20)
    if isinstance(rq, dict):
        _process_assessment_dict(rq, result)

    # Handle formative/summative split
    if isinstance(am, dict):
        formative = am.get('formative')
        summative = am.get('summative')
        if formative:
            result['formative_assessments'] = formative
        if summative:
            result['summative_assessments'] = summative

    return result if result else None


def _process_assessment_dict(am, result):
    """Process an assessment dict into the result."""
    # MCQs
    mcq = am.get('multiple_choice_questions') or am.get('multiple_choice')
    if mcq is not None:
        if isinstance(mcq, int):
            result['multiple_choice_questions'] = {"count": mcq}
        elif isinstance(mcq, list):
            result['multiple_choice_questions'] = {"count": len(mcq), "items": mcq}
        elif isinstance(mcq, dict):
            result['multiple_choice_questions'] = mcq  # Already has count/topics

    # Short answer
    sa = am.get('short_answer_questions') or am.get('short_answer')
    if sa is not None:
        if isinstance(sa, int):
            result['short_answer_questions'] = {"count": sa}
        elif isinstance(sa, list):
            result['short_answer_questions'] = {"count": len(sa), "items": sa}
        elif isinstance(sa, dict):
            result['short_answer_questions'] = sa

    # Case study exercises
    for key in ['case_study_exercises', 'case_analysis_exercises', 'case_study_analyses',
                'case_based_exercises']:
        cse = am.get(key)
        if cse is not None:
            if isinstance(cse, int):
                result['case_study_exercises'] = {"count": cse}
            elif isinstance(cse, list):
                result['case_study_exercises'] = {"count": len(cse), "items": cse}
            elif isinstance(cse, dict):
                result['case_study_exercises'] = cse
            break

    # Policy analysis
    for key in ['policy_analysis_exercises', 'policy_analysis_scenarios',
                'policy_application_scenarios', 'policy_analysis']:
        pa = am.get(key)
        if pa is not None:
            if isinstance(pa, int):
                result['policy_analysis_exercises'] = {"count": pa}
            elif isinstance(pa, list):
                result['policy_analysis_exercises'] = {"count": len(pa), "items": pa}
            elif isinstance(pa, dict):
                result['policy_analysis_exercises'] = pa
            break

    # Discussion questions
    dq = am.get('discussion_questions')
    if dq is not None:
        if isinstance(dq, int):
            result['discussion_questions'] = {"count": dq}
        elif isinstance(dq, list):
            result['discussion_questions'] = {"count": len(dq), "items": dq}

    # Data interpretation
    di = am.get('data_interpretation_exercises')
    if di is not None:
        if isinstance(di, int):
            result['data_interpretation_exercises'] = {"count": di}
        elif isinstance(di, list):
            result['data_interpretation_exercises'] = {"count": len(di), "items": di}

    # Calculation problems
    cp = am.get('calculation_problems')
    if cp is not None:
        if isinstance(cp, int):
            result['calculation_problems'] = {"count": cp}
        elif isinstance(cp, list):
            result['calculation_problems'] = {"count": len(cp), "items": cp}

    # Critical thinking
    ct = am.get('critical_thinking_scenarios')
    if ct is not None:
        if isinstance(ct, int):
            result['critical_thinking_scenarios'] = {"count": ct}
        elif isinstance(ct, list):
            result['critical_thinking_scenarios'] = {"count": len(ct), "items": ct}

    # Practical applications (ch 13)
    pa2 = am.get('practical_applications')
    if pa2 is not None:
        if isinstance(pa2, int):
            result['practical_exercises'] = {"count": pa2}
        elif isinstance(pa2, list):
            result['practical_exercises'] = {"count": len(pa2), "items": pa2}

    # Exercises (ch 28)
    ex = am.get('exercises')
    if ex is not None:
        if isinstance(ex, list):
            result['practical_exercises'] = {"count": len(ex), "items": ex}

    # Policy analysis exercise (singular, ch 28)
    pae = am.get('policy_analysis_exercise')
    if pae is not None:
        if isinstance(pae, dict):
            result['policy_analysis_exercises'] = {"count": 1, "items": [pae]}


def normalize_key_terms(data):
    """Normalize glossary_terms, key_concepts_and_definitions, key_terms to unified format."""
    terms = []

    # glossary_terms (ch 10) - array of strings
    gt = data.get('glossary_terms')
    if gt and isinstance(gt, list):
        for t in gt:
            if isinstance(t, str):
                terms.append({"term": t})

    # key_concepts_and_definitions (ch 28) - array of {term, definition}
    kcd = data.get('key_concepts_and_definitions')
    if kcd and isinstance(kcd, list):
        for item in kcd:
            if isinstance(item, dict):
                terms.append({"term": item.get('term', ''), "definition": item.get('definition', '')})

    # key_terms (various) - could be array of strings or array of objects
    kt = data.get('key_terms')
    if kt and isinstance(kt, list):
        for item in kt:
            if isinstance(item, str):
                terms.append({"term": item})
            elif isinstance(item, dict):
                terms.append({"term": item.get('term', ''), "definition": item.get('definition', '')})

    return terms if terms else None


def normalize_sdg_alignment(data):
    """Normalize SDG alignment to array of objects."""
    # Check multiple field names
    sdg = data.get('sdg_alignment')
    if sdg is None:
        alignment = data.get('alignment')
        if isinstance(alignment, dict):
            sdg = alignment.get('sustainable_development_goals')

    if sdg is None:
        return None

    if isinstance(sdg, list):
        result = []
        for item in sdg:
            if isinstance(item, str):
                # "SDG 3: Good Health and Well-being (...)"
                m = re.match(r'(SDG\s*\d+)\s*:?\s*(.*)', item)
                if m:
                    result.append({"goal": m.group(1).strip(), "description": m.group(2).strip()})
                else:
                    result.append({"goal": item})
            elif isinstance(item, int):
                result.append({"goal": f"SDG {item}"})
            elif isinstance(item, dict):
                result.append(item)
        return result

    return None


def normalize_content_sections(data):
    """Normalize content_sections / content_structure / major_sections."""
    cs = data.get('content_sections')
    if cs is None:
        # Check content_structure (ch 28)
        cs_struct = data.get('content_structure')
        if isinstance(cs_struct, dict):
            cs = cs_struct.get('sections')

    if cs is None:
        # Check major_sections inside wrapper (ch 1)
        wrapper = get_wrapper(data)
        ms = wrapper.get('major_sections') if isinstance(wrapper, dict) else None
        if ms and isinstance(ms, list):
            return [{"title": s} for s in ms if isinstance(s, str)]

    if cs is None:
        return None

    if isinstance(cs, list):
        result = []
        for section in cs:
            if isinstance(section, dict):
                normalized = {}
                sid = section.get('section_id') or section.get('section_number')
                if sid:
                    normalized['section_id'] = str(sid)
                if 'title' in section:
                    normalized['title'] = section['title']
                wc = section.get('word_count') or section.get('estimated_words')
                if wc:
                    normalized['word_count'] = wc
                if 'subsections' in section:
                    subs = section['subsections']
                    if isinstance(subs, list):
                        normalized['subsections'] = subs
                if 'key_topics' in section:
                    normalized['key_topics'] = section['key_topics']
                if 'figures' in section:
                    normalized['figures'] = section['figures']
                if 'tables' in section:
                    normalized['tables'] = section['tables']
                if 'key_concepts' in section:
                    normalized['key_concepts'] = section['key_concepts']
                if 'primary_references' in section:
                    normalized['primary_references'] = section['primary_references']
                result.append(normalized)
            elif isinstance(section, str):
                result.append({"title": section})
        return result

    return None


def normalize_references(data):
    """Normalize references metadata."""
    refs = data.get('references')
    if refs and isinstance(refs, dict):
        result = {}
        result['total_count'] = refs.get('total_count') or refs.get('total_references')
        if refs.get('primary_sources') is not None:
            result['primary_sources'] = refs['primary_sources']
        if refs.get('secondary_sources') is not None:
            result['secondary_sources'] = refs['secondary_sources']
        if refs.get('primary_source_percentage') is not None:
            result['primary_source_percentage'] = refs['primary_source_percentage']
        # Reference types
        rt = refs.get('reference_types') or refs.get('source_types')
        if rt:
            result['reference_types'] = rt
        # Publication years
        py = refs.get('publication_years') or refs.get('recency')
        if py:
            result['publication_years'] = py
        if refs.get('citation_style'):
            result['citation_style'] = refs['citation_style']
        return {k: v for k, v in result.items() if v is not None}

    # Check references_count (ch 13)
    rc = data.get('references_count')
    if rc and isinstance(rc, int):
        return {"total_count": rc}

    return None


def transform_chapter(filepath):
    """Transform a single chapter metadata file to the unified schema."""
    with open(filepath, 'r') as f:
        data = json.load(f)

    chapter_number, title = extract_chapter_info(data)
    wrapper = get_wrapper(data)

    result = {}

    # 1. Core identity
    result['chapter_number'] = chapter_number
    result['title'] = title

    # 2. Part
    part = parse_part(data)
    if part:
        result['part'] = part

    # 3. Version
    version = wrapper.get('version') or data.get('version')
    if version:
        result['version'] = str(version)

    # 4. Last updated
    lu = wrapper.get('last_updated') or data.get('last_updated')
    if lu:
        result['last_updated'] = lu

    # 5. Abstract
    abstract = data.get('abstract')
    if abstract:
        result['abstract'] = abstract

    # 6. Authors
    authors = wrapper.get('authors') or data.get('authors')
    if authors:
        if isinstance(authors, list):
            normalized_authors = []
            for a in authors:
                if isinstance(a, str):
                    normalized_authors.append({"name": a})
                elif isinstance(a, dict):
                    normalized_authors.append(a)
            result['authors'] = normalized_authors

    # 7. Keywords
    keywords = wrapper.get('keywords') or data.get('keywords')
    if keywords:
        result['keywords'] = keywords

    # 8. Word count target
    wct = parse_word_count_target(data)
    if wct:
        result['word_count_target'] = wct

    # 9. Actual word count
    awc = wrapper.get('actual_word_count') or data.get('actual_word_count')
    if awc:
        result['actual_word_count'] = awc

    # 10. Estimated reading time
    ert = wrapper.get('estimated_reading_time') or data.get('estimated_reading_time')
    if ert:
        result['estimated_reading_time'] = ert

    # 11. Difficulty level
    dl = wrapper.get('difficulty_level') or data.get('difficulty_level')
    if dl:
        result['difficulty_level'] = dl.lower() if isinstance(dl, str) else dl

    # 12. Citation style
    cs_style = wrapper.get('citation_style') or data.get('citation_style')
    ct = wrapper.get('citation_target')
    if cs_style:
        result['citation_style'] = cs_style
    elif isinstance(ct, dict) and ct.get('style'):
        result['citation_style'] = ct['style']

    # 13. Reference count target
    rct = parse_reference_count_target(data)
    if rct:
        result['reference_count_target'] = rct

    # 14. Evidence level
    el = data.get('evidence_level')
    if el:
        result['evidence_level'] = el

    # 15. Review status
    rs = data.get('review_status')
    if rs:
        result['review_status'] = rs

    # 16. Estimated completion date
    ecd = data.get('estimated_completion_date')
    if ecd:
        result['estimated_completion_date'] = ecd

    # 17. Overview
    overview = data.get('overview')
    if overview:
        result['overview'] = overview

    # 18. Prerequisites
    prereqs = wrapper.get('prerequisites') or data.get('prerequisites')
    if prereqs:
        result['prerequisites'] = prereqs

    # 19. Prerequisite chapters
    pc = data.get('prerequisite_chapters')
    if pc:
        result['prerequisite_chapters'] = pc

    # 20. Related chapters
    rc = data.get('related_chapters')
    if rc:
        result['related_chapters'] = rc

    # 21. Preceding/following chapter
    prec = wrapper.get('preceding_chapter') or data.get('preceding_chapter')
    foll = wrapper.get('following_chapter') or data.get('following_chapter')
    if prec:
        result['preceding_chapter'] = prec
    if foll:
        result['following_chapter'] = foll

    # 22. Cross references
    cr = data.get('cross_references')
    if cr:
        result['cross_references'] = cr

    # 23. Learning objectives
    lo = normalize_learning_objectives(data)
    if lo:
        result['learning_objectives'] = lo

    # 24. Key concepts (simple string array)
    kc = (wrapper.get('key_concepts') if isinstance(wrapper, dict) else None) or data.get('key_concepts')
    if kc and isinstance(kc, list):
        result['key_concepts'] = kc

    # 25. Key terms (with definitions)
    kt = normalize_key_terms(data)
    if kt:
        result['key_terms'] = kt

    # 26. Key topics (structured)
    key_topics = data.get('key_topics')
    if key_topics is None:
        key_topics = wrapper.get('key_topics') if isinstance(wrapper, dict) else None
    if key_topics:
        if isinstance(key_topics, list):
            normalized_topics = []
            for t in key_topics:
                if isinstance(t, str):
                    normalized_topics.append({"topic": t})
                elif isinstance(t, dict):
                    normalized_topics.append(t)
            result['key_topics'] = normalized_topics
        elif isinstance(key_topics, dict):
            # Object keyed by topic name (ch 22)
            normalized_topics = []
            for topic_key, topic_val in key_topics.items():
                entry = {"topic": topic_key.replace('_', ' ').title()}
                if isinstance(topic_val, dict):
                    if 'subtopics' in topic_val:
                        entry['subtopics'] = topic_val['subtopics']
                    if 'global_examples' in topic_val:
                        entry['global_examples'] = topic_val['global_examples']
                    if 'assessment_methods' in topic_val:
                        entry['assessment_methods'] = topic_val['assessment_methods']
                    if 'methodologies' in topic_val:
                        entry['methodologies'] = topic_val['methodologies']
                    if 'applications' in topic_val:
                        entry['applications'] = topic_val['applications']
                    if 'global_frameworks' in topic_val:
                        entry['global_frameworks'] = topic_val['global_frameworks']
                    if 'implementation_challenges' in topic_val:
                        entry['implementation_challenges'] = topic_val['implementation_challenges']
                    if 'integration_approaches' in topic_val:
                        entry['integration_approaches'] = topic_val['integration_approaches']
                    if 'indicators' in topic_val:
                        entry['indicators'] = topic_val['indicators']
                normalized_topics.append(entry)
            result['key_topics'] = normalized_topics

    # 27. Theoretical frameworks
    tf = data.get('theoretical_frameworks')
    if tf:
        result['theoretical_frameworks'] = tf

    # 28. Content sections
    content_secs = normalize_content_sections(data)
    if content_secs:
        result['content_sections'] = content_secs

    # 29. Chapter structure (ch 6)
    ch_struct = data.get('chapter_structure')
    if ch_struct:
        result['chapter_structure'] = ch_struct

    # 30. Case studies
    case_studies = normalize_case_studies(data)
    if case_studies:
        result['case_studies'] = case_studies

    # 31. Geographic coverage
    geo = normalize_geographic_coverage(data)
    if geo:
        result['geographic_coverage'] = geo

    # 32. SDG alignment
    sdg = normalize_sdg_alignment(data)
    if sdg:
        result['sdg_alignment'] = sdg

    # 33. Cross-cutting themes
    cct = data.get('cross_cutting_themes')
    if cct:
        result['cross_cutting_themes'] = cct

    # 34. Competencies addressed
    comp = data.get('competencies_addressed') or data.get('competencies')
    if comp:
        result['competencies_addressed'] = comp

    # 35. Technical skills
    ts = data.get('technical_skills')
    if ts:
        result['technical_skills'] = ts

    # 36. Ethical considerations
    ec = data.get('ethical_considerations')
    if ec:
        result['ethical_considerations'] = ec

    # 37. Practical applications (top-level, ch 6)
    pa = data.get('practical_applications')
    if pa:
        result['practical_applications'] = pa

    # 38. Practical exercises (top-level, ch 20)
    pe = data.get('practical_exercises')
    if pe:
        result['practical_exercises'] = pe

    # 39. Key frameworks
    kf = data.get('key_frameworks')
    if kf:
        result['key_frameworks'] = kf

    # 40. Multimedia elements
    me = data.get('multimedia_elements') or data.get('multimedia_resources')
    if me:
        result['multimedia_elements'] = me

    # 41. Assessment materials
    am = normalize_assessment_materials(data)
    if am:
        result['assessment_materials'] = am

    # 42. References metadata
    refs = normalize_references(data)
    if refs:
        result['references'] = refs

    # 43. Required readings
    rr = data.get('required_readings')
    if rr:
        result['required_readings'] = rr

    # 44. Supplementary resources
    sr = data.get('supplementary_resources')
    if sr:
        result['supplementary_resources'] = sr

    # 45. Resources (ch 12)
    res = data.get('resources')
    if res:
        result['resources'] = res

    # 46. References framework (ch 28)
    rf = data.get('references_framework')
    if rf:
        result['references_framework'] = rf

    # 47. Research emphasis (ch 22)
    re_data = data.get('research_emphasis')
    if re_data:
        result['research_emphasis'] = re_data

    # 48. Sustainability integration (ch 22)
    si = data.get('sustainability_integration')
    if si:
        result['sustainability_integration'] = si

    # 49. Quality metrics
    qm = data.get('quality_metrics')
    if qm:
        result['quality_metrics'] = qm

    # 50. WHO frameworks (from alignment, ch 10)
    alignment = data.get('alignment')
    if isinstance(alignment, dict) and 'who_frameworks' in alignment:
        result['who_frameworks'] = alignment['who_frameworks']

    # 51. Global representation (ch 15 - string)
    gr = data.get('global_representation')
    if gr and isinstance(gr, str):
        result['global_representation'] = gr

    return result


def main():
    """Process all 35 chapter metadata files."""
    for i in range(1, 36):
        filename = f'chapter_{i:02d}_metadata.json'
        filepath = os.path.join(CHAPTERS_DIR, filename)

        if not os.path.exists(filepath):
            print(f'WARNING: {filename} not found, skipping')
            continue

        print(f'Processing {filename}...', end=' ')
        try:
            result = transform_chapter(filepath)

            # Verify chapter number matches filename
            if result.get('chapter_number') != i:
                print(f'WARNING: chapter_number {result.get("chapter_number")} != expected {i}')

            # Write back
            with open(filepath, 'w') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
                f.write('\n')

            print('OK')
        except Exception as e:
            print(f'ERROR: {e}')
            raise


if __name__ == '__main__':
    main()
