"""
Interactive 401(k) Advisor - Unified RAG + Fund SQL Pipeline.

Automatically routes queries to the right pipeline:
- RAG: Plan documents, rules, procedures
- Fund: Fees, returns, comparisons
- Hybrid: Both

Run: python src/interactive_rag.py
"""

from dispatcher import UnifiedDispatcher

print("Loading unified 401(k) advisor...")
dispatcher = UnifiedDispatcher(verbose=False)
print("Ready!\n")


def main():
    print("=" * 60)
    print("401(k) Advisor - Ask me anything about your plan")
    print("=" * 60)
    print("Commands:")
    print("  Type a question and press Enter")
    print("  'sources' - toggle showing sources")
    print("  'debug'   - toggle debug mode (shows routing)")
    print("  'quit'    - exit")
    print("=" * 60)

    show_sources = False
    debug_mode = False

    while True:
        print()
        question = input("You: ").strip()

        if not question:
            continue

        if question.lower() == "quit":
            print("Bye!")
            break

        if question.lower() == "sources":
            show_sources = not show_sources
            print(f"Show sources: {'ON' if show_sources else 'OFF'}")
            continue

        if question.lower() == "debug":
            debug_mode = not debug_mode
            dispatcher.verbose = debug_mode
            print(f"Debug mode: {'ON' if debug_mode else 'OFF'}")
            continue

        try:
            result = dispatcher.ask(question)

            print(f"\nBot: {result.answer}")

            if show_sources:
                # Show sources for RAG pipeline
                if result.rag_sources:
                    sources = [f"{s['source']} p.{s['page']}" for s in result.rag_sources]
                    print(f"\nSources: {', '.join(sources)}")
                # Show SQL for Fund pipeline
                if result.fund_sql:
                    print(f"\nSQL: {result.fund_sql}")

            if debug_mode:
                c = result.classification
                print(f"\n[Route: {c.query_type} | Confidence: {c.confidence:.0%} | Method: {c.method}]")
                print(f"[Pipelines used: {', '.join(result.pipelines_used)}]")

        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()
