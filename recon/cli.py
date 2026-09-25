from __future__ import annotations
import argparse
from pathlib import Path
from .engine import assess_trajectory, detect_changes, load_sources, normalize, render_report

def main() -> int:
    parser=argparse.ArgumentParser(prog="recon",description="Commercial Reality Reconnaissance v0.1")
    sub=parser.add_subparsers(dest="command",required=True)
    scan=sub.add_parser("scan",help="scan curated source records")
    scan.add_argument("--input",type=Path,required=True)
    scan.add_argument("--subject")
    scan.add_argument("--output",type=Path)
    args=parser.parse_args()
    if args.command=="scan":
        records=load_sources(args.input); observations=normalize(records); changes=detect_changes(observations)
        subject=args.subject or (observations[0].subject_id if observations else "unknown")
        report=render_report(records,observations,changes,assess_trajectory(subject,observations,changes))
        if args.output: args.output.write_text(report)
        else: print(report,end="")
        return 0
    return 1

if __name__=="__main__": raise SystemExit(main())
