from agents.generator import generator_agent
from agents.reviewer import reviewer_agent


def run_pipeline(grade, topic):
    gen_output = generator_agent(grade, topic)

    review = reviewer_agent(gen_output, grade)

    if review["status"] == "fail":
        refined = generator_agent(grade, topic, review["feedback"])
        return {
            "initial": gen_output,
            "review": review,
            "refined": refined
        }

    return {
        "initial": gen_output,
        "review": review
    }


if __name__ == "__main__":
    result = run_pipeline(4, "Types of angles")
    print(result)