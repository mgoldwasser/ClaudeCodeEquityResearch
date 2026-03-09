#!/usr/bin/env python3
"""
Sentiment & Tone Analyzer for Earnings Transcripts
===================================================
Analyzes management language for hedging, confidence, uncertainty,
and red flags in earnings call transcripts and press releases.

Usage:
    python tools/sentiment-analyzer.py analyze --file transcript.txt
    python tools/sentiment-analyzer.py compare --file1 q1_transcript.txt --file2 q2_transcript.txt
    python tools/sentiment-analyzer.py score --file transcript.txt
    python tools/sentiment-analyzer.py score --text "We believe revenue may approximately reach..."
    python tools/sentiment-analyzer.py red-flags --file transcript.txt
    python tools/sentiment-analyzer.py guidance --file transcript.txt
"""

import argparse
import json
import re
import sys
from collections import Counter
from typing import Dict, List, Tuple, Optional


# ============================================================
# WORD LISTS (Loughran-McDonald Financial Sentiment Subset)
# ============================================================

HEDGING_WORDS = [
    "approximately", "roughly", "about", "around", "estimated",
    "we believe", "we think", "we expect", "we anticipate",
    "may", "might", "could", "possibly", "potentially",
    "likely", "unlikely", "probable", "uncertain", "uncertainty",
    "subject to", "depends on", "contingent", "conditional",
    "generally", "typically", "tends to", "in most cases",
    "somewhat", "relatively", "fairly", "moderately",
    "to some extent", "in part", "partially",
    "cautiously optimistic", "guardedly", "conservative estimate",
    "range of outcomes", "variability", "volatility",
    "difficult to predict", "hard to forecast", "challenging to quantify",
    "working through", "navigating", "managing through",
]

CERTAINTY_WORDS = [
    "definitely", "certainly", "clearly", "obviously", "undoubtedly",
    "will", "shall", "committed to", "committed", "guarantee",
    "confident", "very confident", "highly confident", "strong confidence",
    "absolutely", "unquestionably", "without doubt",
    "proven", "demonstrated", "established", "validated",
    "on track", "ahead of schedule", "exceeding expectations",
    "delivering", "executing", "achieved", "accomplished",
    "robust", "strong", "exceptional", "outstanding", "excellent",
    "significant", "substantial", "meaningful", "transformative",
    "accelerating", "momentum", "inflection point",
]

NEGATIVE_FINANCIAL_WORDS = [
    "loss", "losses", "decline", "declined", "declining",
    "deterioration", "deteriorated", "weakened", "weakness",
    "impairment", "impaired", "write-down", "write-off", "writedown",
    "restructuring", "restructured", "downsizing", "layoff", "layoffs",
    "litigation", "lawsuit", "regulatory action", "investigation",
    "default", "delinquent", "delinquency", "bankruptcy",
    "recession", "recessionary", "downturn", "contraction",
    "headwind", "headwinds", "pressure", "pressured", "compressed",
    "shortfall", "miss", "missed", "below expectations",
    "challenge", "challenges", "challenging", "difficult", "difficulty",
    "risk", "risks", "risky", "exposure", "vulnerability",
    "concern", "concerned", "concerning", "worried", "worry",
    "disappointing", "disappointed", "underperformed", "underperformance",
    "adverse", "unfavorable", "negative", "negatively",
    "slowdown", "slowed", "slowing", "deceleration", "decelerated",
]

POSITIVE_FINANCIAL_WORDS = [
    "growth", "growing", "grew", "gain", "gains", "gained",
    "improvement", "improved", "improving", "strengthened",
    "record", "all-time high", "milestone", "breakthrough",
    "profit", "profitable", "profitability", "margin expansion",
    "upgrade", "upgraded", "outperform", "outperformed", "outperformance",
    "tailwind", "tailwinds", "benefit", "benefiting", "benefited",
    "exceed", "exceeded", "exceeding", "beat", "beating",
    "upside", "opportunity", "opportunities", "favorable",
    "innovation", "innovative", "differentiated", "competitive advantage",
    "market share", "share gains", "winning", "won",
    "demand", "strong demand", "robust demand", "healthy demand",
    "pipeline", "backlog", "order book", "bookings",
    "recovery", "recovering", "rebound", "rebounded",
    "expansion", "expanding", "expanded", "launch", "launched",
]

FORWARD_LOOKING_PHRASES = [
    "going forward", "looking ahead", "in the coming",
    "next quarter", "next year", "full year", "fiscal year",
    "we expect", "we anticipate", "we project", "we forecast",
    "our outlook", "our guidance", "our target", "our goal",
    "pipeline", "roadmap", "planned", "planning to",
    "will be", "will continue", "will drive", "will deliver",
    "positioned to", "poised to", "set to", "on track to",
    "future", "long-term", "medium-term", "near-term",
]

BACKWARD_LOOKING_PHRASES = [
    "last quarter", "last year", "prior year", "previous quarter",
    "year-over-year", "quarter-over-quarter", "sequential",
    "we achieved", "we delivered", "we reported", "we generated",
    "compared to", "versus", "relative to prior",
    "historically", "in the past", "traditionally",
    "year ago", "quarter ago", "months ago",
]

EVASION_PATTERNS = [
    r"that's a great question",
    r"let me (turn|hand) (it|that) over to",
    r"i('d| would) (rather|prefer) not (to )?(comment|speculate|get into)",
    r"we('re| are) not (going to |prepared to )?(provide|give|share|disclose)",
    r"it('s| is) (too early|premature) to",
    r"we('ll| will) (have|provide) more (details|color|information) (on|at|in)",
    r"i (don't|do not) (want to|have) (get ahead|speculate)",
    r"as (i|we) (said|mentioned) (earlier|before|previously)",
    r"(next|following|subsequent) question",
    r"let('s| us) move on",
]

NON_ANSWER_PATTERNS = [
    r"we('re| are) focused on",
    r"our (strategy|approach|plan) (is|remains|continues)",
    r"we continue to (believe|focus|invest|execute)",
    r"that('s| is) (consistent|in line) with our",
    r"we('re| are) (pleased|excited|proud) (with|about|to)",
    r"as (you|we) know",
]


# ============================================================
# ANALYSIS FUNCTIONS
# ============================================================

def count_phrase_matches(text: str, phrases: List[str]) -> Tuple[int, List[str]]:
    """Count occurrences of phrases in text, return count and matched phrases."""
    text_lower = text.lower()
    count = 0
    matched = []
    for phrase in phrases:
        occurrences = text_lower.count(phrase.lower())
        if occurrences > 0:
            count += occurrences
            matched.append(f"{phrase} ({occurrences}x)")
    return count, matched


def analyze_hedging(text: str) -> Dict:
    """Analyze hedging language density."""
    count, matched = count_phrase_matches(text, HEDGING_WORDS)
    word_count = len(text.split())
    density = count / max(word_count, 1) * 1000  # per 1000 words

    if density > 15:
        assessment = "HIGH hedging density — management is being unusually cautious"
    elif density > 8:
        assessment = "MODERATE hedging density — normal range for earnings calls"
    else:
        assessment = "LOW hedging density — management is speaking with relative certainty"

    return {
        "hedging_count": count,
        "hedging_density_per_1000_words": round(density, 1),
        "assessment": assessment,
        "top_hedging_phrases": matched[:15],
    }


def analyze_certainty(text: str) -> Dict:
    """Analyze certainty/confidence language density."""
    count, matched = count_phrase_matches(text, CERTAINTY_WORDS)
    word_count = len(text.split())
    density = count / max(word_count, 1) * 1000

    if density > 12:
        assessment = "HIGH certainty language — management is very confident (verify if justified)"
    elif density > 5:
        assessment = "MODERATE certainty language — normal confidence level"
    else:
        assessment = "LOW certainty language — management may be unsure or cautious"

    return {
        "certainty_count": count,
        "certainty_density_per_1000_words": round(density, 1),
        "assessment": assessment,
        "top_certainty_phrases": matched[:15],
    }


def confidence_ratio(text: str) -> Dict:
    """
    Ratio of certainty to hedging language.
    > 1.5: Highly confident
    0.8-1.5: Balanced
    < 0.8: More hedging than certainty
    """
    hedge_count, _ = count_phrase_matches(text, HEDGING_WORDS)
    cert_count, _ = count_phrase_matches(text, CERTAINTY_WORDS)
    total = hedge_count + cert_count

    ratio = cert_count / max(hedge_count, 1)

    if ratio > 1.5:
        assessment = "CONFIDENT — certainty language dominates hedging"
    elif ratio > 0.8:
        assessment = "BALANCED — normal mix of certainty and hedging"
    else:
        assessment = "CAUTIOUS — hedging language dominates certainty"

    return {
        "certainty_count": cert_count,
        "hedging_count": hedge_count,
        "ratio": round(ratio, 2),
        "assessment": assessment,
    }


def forward_backward_ratio(text: str) -> Dict:
    """Ratio of forward-looking to backward-looking statements."""
    fwd_count, fwd_matched = count_phrase_matches(text, FORWARD_LOOKING_PHRASES)
    bwd_count, bwd_matched = count_phrase_matches(text, BACKWARD_LOOKING_PHRASES)

    ratio = fwd_count / max(bwd_count, 1)

    if ratio > 2.0:
        assessment = "VERY FORWARD-LOOKING — management focused on future (positive for growth story)"
    elif ratio > 1.0:
        assessment = "FORWARD-LEANING — balanced with slight future orientation"
    elif ratio > 0.5:
        assessment = "BACKWARD-LEANING — management discussing past more than future"
    else:
        assessment = "PAST-FOCUSED — unusually focused on past results (may be avoiding future guidance)"

    return {
        "forward_looking_count": fwd_count,
        "backward_looking_count": bwd_count,
        "ratio": round(ratio, 2),
        "assessment": assessment,
    }


def sentiment_score(text: str) -> Dict:
    """
    Net sentiment score based on financial word lists.
    Score ranges from -100 (very negative) to +100 (very positive).
    """
    pos_count, pos_matched = count_phrase_matches(text, POSITIVE_FINANCIAL_WORDS)
    neg_count, neg_matched = count_phrase_matches(text, NEGATIVE_FINANCIAL_WORDS)
    total = pos_count + neg_count

    if total == 0:
        net_score = 0
    else:
        net_score = ((pos_count - neg_count) / total) * 100

    word_count = len(text.split())

    if net_score > 40:
        assessment = "VERY POSITIVE tone — verify against actual financial results"
    elif net_score > 10:
        assessment = "POSITIVE tone — generally constructive language"
    elif net_score > -10:
        assessment = "NEUTRAL tone — balanced positive and negative language"
    elif net_score > -40:
        assessment = "NEGATIVE tone — more negative language than positive"
    else:
        assessment = "VERY NEGATIVE tone — significant negative language density"

    return {
        "positive_word_count": pos_count,
        "negative_word_count": neg_count,
        "net_sentiment_score": round(net_score, 1),
        "sentiment_per_1000_words": round(total / max(word_count, 1) * 1000, 1),
        "assessment": assessment,
        "top_positive": pos_matched[:10],
        "top_negative": neg_matched[:10],
    }


def management_tone_score(text: str) -> Dict:
    """
    Composite management tone score (0-100).
    Combines confidence ratio, sentiment, and forward-looking orientation.
    """
    conf = confidence_ratio(text)
    sent = sentiment_score(text)
    fwd = forward_backward_ratio(text)

    # Normalize components to 0-100 scale
    # Confidence ratio: 0-3 → 0-100
    conf_score = min(conf["ratio"] / 3.0 * 100, 100)
    # Sentiment: -100 to +100 → 0-100
    sent_score = (sent["net_sentiment_score"] + 100) / 2
    # Forward ratio: 0-4 → 0-100
    fwd_score = min(fwd["ratio"] / 4.0 * 100, 100)

    # Weighted composite
    composite = conf_score * 0.40 + sent_score * 0.35 + fwd_score * 0.25

    if composite > 75:
        assessment = "VERY CONFIDENT — management is highly positive and forward-looking"
    elif composite > 55:
        assessment = "CONFIDENT — management tone is constructive"
    elif composite > 40:
        assessment = "NEUTRAL — balanced tone without strong directional signals"
    elif composite > 25:
        assessment = "CAUTIOUS — management tone suggests uncertainty or concern"
    else:
        assessment = "DEFENSIVE — management is hedging heavily and focused on past"

    return {
        "composite_score": round(composite, 1),
        "components": {
            "confidence_component": round(conf_score, 1),
            "sentiment_component": round(sent_score, 1),
            "forward_looking_component": round(fwd_score, 1),
        },
        "weights": "confidence 40%, sentiment 35%, forward-looking 25%",
        "assessment": assessment,
    }


def detect_red_flags(text: str) -> Dict:
    """Detect evasion patterns, non-answers, and concerning language."""
    text_lower = text.lower()

    evasions = []
    for pattern in EVASION_PATTERNS:
        matches = re.findall(pattern, text_lower)
        if matches:
            # Find the actual text around the match
            for m in re.finditer(pattern, text_lower):
                start = max(0, m.start() - 30)
                end = min(len(text_lower), m.end() + 30)
                context = text[start:end].strip()
                evasions.append(f"...{context}...")

    non_answers = []
    for pattern in NON_ANSWER_PATTERNS:
        matches = re.findall(pattern, text_lower)
        if matches:
            for m in re.finditer(pattern, text_lower):
                start = max(0, m.start() - 30)
                end = min(len(text_lower), m.end() + 30)
                context = text[start:end].strip()
                non_answers.append(f"...{context}...")

    # Check for unusual patterns
    unusual = []
    # Excessive use of "as I mentioned" (repeating themselves = nervous)
    as_mentioned = len(re.findall(r"as (i|we) (mentioned|said|noted)", text_lower))
    if as_mentioned > 3:
        unusual.append(f"Repeated self-references ({as_mentioned}x) — may indicate nervousness or deflection")

    # Passing to others frequently
    hand_offs = len(re.findall(r"(let me|i'll) (turn|hand|pass) (it|that|this) (over |back )?(to)", text_lower))
    if hand_offs > 4:
        unusual.append(f"Frequent hand-offs to others ({hand_offs}x) — CEO may be avoiding certain topics")

    # Excessive qualifiers
    qualifier_count = len(re.findall(r"\b(sort of|kind of|a little bit|in a way|if you will)\b", text_lower))
    if qualifier_count > 5:
        unusual.append(f"Excessive qualifiers ({qualifier_count}x) — language suggests imprecision or discomfort")

    total_flags = len(evasions) + len(non_answers) + len(unusual)

    if total_flags > 8:
        assessment = "MULTIPLE RED FLAGS — significant evasion and deflection detected"
    elif total_flags > 4:
        assessment = "SOME CONCERNS — notable evasion patterns present"
    elif total_flags > 0:
        assessment = "MINOR FLAGS — few evasion patterns (may be normal)"
    else:
        assessment = "CLEAN — no significant evasion patterns detected"

    return {
        "total_red_flags": total_flags,
        "assessment": assessment,
        "evasion_instances": evasions[:10],
        "non_answer_instances": non_answers[:10],
        "unusual_patterns": unusual,
    }


def extract_guidance(text: str) -> Dict:
    """Extract quantitative guidance statements from transcript."""
    guidance_patterns = [
        # Revenue/earnings guidance
        r"(?:revenue|sales|earnings|eps|ebitda|income|margin)[\s\S]{0,50}?(?:guidance|outlook|expect|target|range|forecast)[\s\S]{0,80}?\$?[\d,.]+",
        # Expect X to Y
        r"(?:we )?expect\w*\s+[\s\S]{0,60}?\$?[\d,.]+\s*(?:to|and|-)\s*\$?[\d,.]+",
        # Range of X to Y
        r"(?:range|guidance)\s+(?:of|is|at)\s+\$?[\d,.]+\s*(?:to|and|-)\s*\$?[\d,.]+",
        # Growth of X%
        r"(?:growth|increase|decline|decrease)\s+(?:of\s+)?(?:approximately\s+)?[\d,.]+\s*%",
        # Margin of X%
        r"(?:margin|margins)\s+(?:of|at|around|approximately)\s+[\d,.]+\s*%",
        # Raising/lowering/maintaining guidance
        r"(?:raising|lowering|maintaining|reaffirming|narrowing)\s+(?:our\s+)?(?:guidance|outlook|forecast|target)",
    ]

    statements = []
    text_lower = text.lower()

    for pattern in guidance_patterns:
        for match in re.finditer(pattern, text_lower):
            start = max(0, match.start() - 20)
            end = min(len(text), match.end() + 20)
            context = text[start:end].strip()
            if len(context) > 20:  # Filter noise
                statements.append(f"...{context}...")

    # Deduplicate similar statements
    unique_statements = []
    for s in statements:
        if not any(s[:30] in u for u in unique_statements):
            unique_statements.append(s)

    # Detect guidance direction
    raising = len(re.findall(r"\b(raising|raised|increased|higher|upward)\b.{0,30}\b(guidance|outlook|forecast)\b", text_lower))
    lowering = len(re.findall(r"\b(lowering|lowered|decreased|reduced|downward)\b.{0,30}\b(guidance|outlook|forecast)\b", text_lower))
    maintaining = len(re.findall(r"\b(maintaining|reaffirming|unchanged|consistent)\b.{0,30}\b(guidance|outlook|forecast)\b", text_lower))

    if raising > 0 and lowering == 0:
        direction = "RAISING guidance — positive signal"
    elif lowering > 0 and raising == 0:
        direction = "LOWERING guidance — negative signal"
    elif maintaining > 0:
        direction = "MAINTAINING guidance — neutral signal"
    elif raising > 0 and lowering > 0:
        direction = "MIXED — raising some metrics, lowering others"
    else:
        direction = "UNCLEAR — no explicit guidance direction detected"

    return {
        "guidance_statements_found": len(unique_statements),
        "guidance_direction": direction,
        "direction_counts": {"raising": raising, "lowering": lowering, "maintaining": maintaining},
        "extracted_statements": unique_statements[:15],
    }


def full_analysis(text: str) -> Dict:
    """Complete sentiment analysis of a transcript or document."""
    word_count = len(text.split())

    return {
        "document_stats": {
            "word_count": word_count,
            "estimated_pages": round(word_count / 300, 1),
        },
        "management_tone": management_tone_score(text),
        "confidence_analysis": confidence_ratio(text),
        "hedging_analysis": analyze_hedging(text),
        "certainty_analysis": analyze_certainty(text),
        "sentiment": sentiment_score(text),
        "forward_vs_backward": forward_backward_ratio(text),
        "red_flags": detect_red_flags(text),
        "guidance": extract_guidance(text),
    }


def compare_transcripts(text1: str, text2: str) -> Dict:
    """Compare two transcripts (e.g., current vs. prior quarter)."""
    analysis1 = full_analysis(text1)
    analysis2 = full_analysis(text2)

    # Calculate deltas
    tone_delta = (
        analysis1["management_tone"]["composite_score"] -
        analysis2["management_tone"]["composite_score"]
    )
    conf_delta = (
        analysis1["confidence_analysis"]["ratio"] -
        analysis2["confidence_analysis"]["ratio"]
    )
    sent_delta = (
        analysis1["sentiment"]["net_sentiment_score"] -
        analysis2["sentiment"]["net_sentiment_score"]
    )
    fwd_delta = (
        analysis1["forward_vs_backward"]["ratio"] -
        analysis2["forward_vs_backward"]["ratio"]
    )
    flag_delta = (
        analysis1["red_flags"]["total_red_flags"] -
        analysis2["red_flags"]["total_red_flags"]
    )

    # Significant shifts
    shifts = []
    if abs(tone_delta) > 10:
        direction = "improved" if tone_delta > 0 else "deteriorated"
        shifts.append(f"Management tone {direction} by {abs(tone_delta):.1f} points")
    if abs(conf_delta) > 0.3:
        direction = "increased" if conf_delta > 0 else "decreased"
        shifts.append(f"Confidence ratio {direction} from {analysis2['confidence_analysis']['ratio']:.2f} to {analysis1['confidence_analysis']['ratio']:.2f}")
    if abs(sent_delta) > 15:
        direction = "more positive" if sent_delta > 0 else "more negative"
        shifts.append(f"Sentiment shifted {direction} by {abs(sent_delta):.1f} points")
    if flag_delta > 2:
        shifts.append(f"Red flags increased by {flag_delta} — potential concern")
    elif flag_delta < -2:
        shifts.append(f"Red flags decreased by {abs(flag_delta)} — positive improvement")

    return {
        "current_period": {
            "tone_score": analysis1["management_tone"]["composite_score"],
            "confidence_ratio": analysis1["confidence_analysis"]["ratio"],
            "sentiment_score": analysis1["sentiment"]["net_sentiment_score"],
            "red_flags": analysis1["red_flags"]["total_red_flags"],
        },
        "prior_period": {
            "tone_score": analysis2["management_tone"]["composite_score"],
            "confidence_ratio": analysis2["confidence_analysis"]["ratio"],
            "sentiment_score": analysis2["sentiment"]["net_sentiment_score"],
            "red_flags": analysis2["red_flags"]["total_red_flags"],
        },
        "deltas": {
            "tone_delta": round(tone_delta, 1),
            "confidence_delta": round(conf_delta, 2),
            "sentiment_delta": round(sent_delta, 1),
            "forward_looking_delta": round(fwd_delta, 2),
            "red_flag_delta": flag_delta,
        },
        "significant_shifts": shifts if shifts else ["No significant shifts detected between periods"],
        "overall_assessment": (
            "IMPROVING" if tone_delta > 5 and sent_delta > 5 else
            "DETERIORATING" if tone_delta < -5 and sent_delta < -5 else
            "STABLE"
        ),
    }


# ============================================================
# CLI INTERFACE
# ============================================================

def read_file_or_text(args) -> str:
    """Read text from file or inline text argument."""
    if hasattr(args, 'file') and args.file:
        with open(args.file, 'r') as f:
            return f.read()
    elif hasattr(args, 'text') and args.text:
        return args.text
    else:
        print("Error: Provide --file or --text", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Sentiment & Tone Analyzer for Earnings Transcripts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  analyze      Full sentiment analysis of a transcript
  compare      Compare two transcripts (current vs. prior)
  score        Quick composite tone score
  red-flags    Detect evasion and non-answer patterns
  guidance     Extract quantitative guidance statements
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Analysis command")

    # Analyze
    analyze_parser = subparsers.add_parser("analyze", help="Full analysis")
    analyze_parser.add_argument("--file", type=str, help="Path to transcript file")
    analyze_parser.add_argument("--text", type=str, help="Inline text to analyze")

    # Compare
    compare_parser = subparsers.add_parser("compare", help="Compare two transcripts")
    compare_parser.add_argument("--file1", type=str, required=True, help="Current period transcript")
    compare_parser.add_argument("--file2", type=str, required=True, help="Prior period transcript")

    # Score
    score_parser = subparsers.add_parser("score", help="Quick tone score")
    score_parser.add_argument("--file", type=str, help="Path to transcript file")
    score_parser.add_argument("--text", type=str, help="Inline text to analyze")

    # Red flags
    rf_parser = subparsers.add_parser("red-flags", help="Detect red flags")
    rf_parser.add_argument("--file", type=str, help="Path to transcript file")
    rf_parser.add_argument("--text", type=str, help="Inline text to analyze")

    # Guidance
    guid_parser = subparsers.add_parser("guidance", help="Extract guidance")
    guid_parser.add_argument("--file", type=str, help="Path to transcript file")
    guid_parser.add_argument("--text", type=str, help="Inline text to analyze")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "analyze":
        text = read_file_or_text(args)
        result = full_analysis(text)

    elif args.command == "compare":
        with open(args.file1, 'r') as f:
            text1 = f.read()
        with open(args.file2, 'r') as f:
            text2 = f.read()
        result = compare_transcripts(text1, text2)

    elif args.command == "score":
        text = read_file_or_text(args)
        result = management_tone_score(text)

    elif args.command == "red-flags":
        text = read_file_or_text(args)
        result = detect_red_flags(text)

    elif args.command == "guidance":
        text = read_file_or_text(args)
        result = extract_guidance(text)

    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
