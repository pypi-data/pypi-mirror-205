#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Use OpenAI to Generate Intent Names """


import os
os.environ['USE_OPENAI'] = str(True)
os.environ['OPENAI_KEY'] = 'gAAAAABiH-eZKbScaS9reXABcCVeRA-VK7rbh-ZBzH72tfzRjTHIH6y5DmcFPxs1Hbf5suJufyD6Z_WhL4h1N1s_BBGpV5JqGZpVCPoB-dAPIFz6gE3uEgUMv_le5RYej5jnZawccsOSKA1RWWpC-CVTcn80S4LehA=='
os.environ['OPENAI_ORG'] = 'gAAAAABiH-0FMWAwMybowrACJ6GPkC91E4DgaV2lJoextMR7U4O5DjB_pw9jBUusuCdH9KEUXp-3Iq-Fni1X-eE6ulSg8JEKtZs-bClX_D-2DyvYpv65iPs='

from pprint import pprint
from openai_helper import chat
from collections import defaultdict
from owl_builder import extract_keyterms
from owl_builder.keyterms.bp import AutoTaxoOrchestrator

from typing import (
    List,
    Optional
)

from baseblock import (
    BaseObject,
    Stopwatch,
    Enforcer,
)

autotaxo_orchestrator = AutoTaxoOrchestrator()


def _keyterms(questions: List[str]) -> List[str]:

    d_questions = {}
    d_questions_rev = defaultdict(list)

    for question in questions:

        terms = autotaxo_orchestrator.keyterms(
            input_text=question,
            use_openai=True,
            use_terms=False,
            use_keyterms=False,
            use_ngrams=False,
            use_nounchunks=False)

        print(question, terms)

        d_questions[question] = terms

    for question in d_questions:
        for term in d_questions[question]:
            d_questions_rev[term].append(question)

    return d_questions, d_questions_rev


def main():
    d_questions, d_questions_rev = _keyterms([
        "What is a typical day in your life like?",
        "Could you outline what you do from morning to night?",
        "Could you tell me about your standard daily routine?",
        "Can you give me a rundown of your daily activities?",
        "What are the tasks you typically complete in a day?",
        "Could you give me a rundown of your daily routine?",
        "Can you give me an idea of your daily activities?",
        "Could you tell me about your typical day-to-day?",
        "How do you go about your day-to-day activities?",
        "How do you typically spend your time each day?",
        "Could you walk me through your daily schedule?",
        "What do you usually do on a day-to-day basis?",
        "What is an ordinary day like for you?",
        "Can you describe your regular daily routine?",
        "How do you fill your hours on a regular day?",
        "What do you typically do throughout the day?",
        "What’s your schedule like on a regular day?",
        "Walk me through a typical day in your life.",
        "What's the usual routine for you each day?",
        "What is a typical day like for you?",
        "What is a typical day like for you?",
        "Can you paint a picture of your usual day?",
        "What does an ordinary day entail for you?",
        "Can you tell me about your daily routine?",
        "What is an usual day like for you?",
        "What does a typical day involve for you?",
        "Give me an idea of what you do in a day.",
        "How do you pass the time during the day?",
        "Can you describe your typical day to me?",
        "How do you structure your time each day?",
        "What’s a typical day like for you?",
        "Describe a day in your typical routine.",
        "What do you do from morning till night?",
        "Tell me about your day-to-day routine.",
        "Walk me through a typical day for you.",
        "What do you usually do during the day?",
        "How do you spend your day-to-day life?",
        "What does your average day consist of?",
        "How do you usually structure your day?",
        "Can you describe a normal day for you?",
        "What does a day in your life involve?",
        "What's the general plan for your day?",
        "Can you detail a typical day for me?",
        "How do you typically spend your day?",
        "Can you describe your daily routine?",
        "How do you usually spend your time?",
        "Tell me about your day-to-day life.",
        "Describe your usual daily schedule.",
        "What is a regular day like for you?",
        "Can you describe your typical day?",
        "How do you spend your average day?",
        "Can you summarize your day for me?",
        "How do you spend your day usually?",
        "What’s a typical day in your life?",
        "Describe a day in your daily life.",
        "What does your day usually entail?",
        "How do you usually spend your day?",
        "Can you describe your daily life?",
        "Walk me through your average day.",
        "Walk me through your average day.",
        "Take me through your typical day.",
        "Talk me through your average day.",
        "What is your usual daily routine?",
        "What is your daily routine like?",
        "What is your daily routine like?",
        "What is a day in your life like?",
        "What's a typical day like?",
        "What's your daily routine like?",
        "What are your daily activities?",
        "Take me through your usual day.",
        "What takes up most of your day?",
        "What does your day consist of?",
        "Walk me through a regular day.",
        "What is a typical day for you?",
        "Detail your daily activities.",
        "How does your day usually go?",
        "Describe your daily schedule.",
        "What's your day-to-day like?",
        "What's a regular day entail?",
        "Describe a day in your life.",
        "How is your day structured?",
        "Outline your daily routine.",
        "Break down your day for me.",
        "What's an average day look?",
        "Describe your typical day.",
        "What does your day entail?",
        "How do you spend your day?",
        "What's a day like for you?",
        "Share your daily schedule.",
        "Narrate your daily events.",
        "What’s your daily routine?",
        "Walk me through your day.",
        "Take me through your day.",
        "How do you fill your day?",
        "Tell me about your day.",
        "Explain your usual day.",
        "Describe a day in life.",
        "How is your day spent?",
        "Walk me through a day.",
        "What fills your day?",
        "What is your day like?",
        "Describe your day?",
        "How's your day been?",
        "What's your typical day like?",
        "Your daily routine?",
        "What's a day like for you?",
        "What's your schedule like today?",
        "What's your day like?",
        "How has your day been so far?",
        "How do you spend your day?",
        "What's your usual day like?",
        "What does your day entail?",
        "What do you do during the day?",
        "Can you walk me through your day?",
        "How's your day shaping up?",
        "What have you been up to today?",
        "What does a typical day for you involve?",
        "What's on your agenda today?",
        "What's your day-to-day like?",
        "What's been the highlight of your day?",
        "How's your day progressing?",
        "What does your average day like?",
        "What's your daily schedule?",
        "What do you usually do during the day?",
        "How do you normally spend your day?",
        "What's your typical daily routine?",
    ])

    pprint(d_questions)
    print()
    pprint(d_questions_rev)


if __name__ == "__main__":
    main()
