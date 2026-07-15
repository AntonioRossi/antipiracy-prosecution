# Written Reply under PCT Rule 43bis.1

## To: International Searching Authority (European Patent Office)
## Re: PCT Application No. PCT/IB2025/051755
## Title: AI-DRIVEN SYSTEM AND METHOD FOR CONTENT DIFFERENTIATION AND PIRACY TRACEABILITY IN STREAMING MEDIA

---

## I. Introduction and Legal Framework

The Applicant respectfully submits this Written Reply pursuant to **PCT Rule 43bis.1(a)(i)** in response to the Written Opinion of the International Searching Authority (ISA) dated 30 April 2025. This reply comprehensively addresses the objections raised under **PCT Article 33(3)** regarding inventive step and demonstrates that the claimed invention satisfies all patentability requirements under the Patent Cooperation Treaty.

The Applicant particularly notes that the ISA has fundamentally misunderstood the invention's use of multi-camera systems, conflating conventional broadcasting applications with the invention's novel security-oriented temporal manipulation. This reply will clarify this critical distinction.

## II. Executive Summary of Key Arguments

Before addressing specific objections, the Applicant emphasizes three fundamental points that the ISA failed to appreciate:

1. **Multi-camera systems are indeed well-known** - the Applicant acknowledges this in paragraphs 21-93 of the specification
2. **The invention repurposes this known infrastructure** for an entirely different technical purpose - security through temporal manipulation
3. **The technical effect achieved** (exponential security scalability without quality loss) is neither taught nor suggested by any prior art use of multi-camera systems

## III. The ISA's Fundamental Misunderstanding

### A. The Multi-Camera Misconception

The ISA's objection that "using multiple cameras is well-known in the art" demonstrates a failure to apply the problem-solution approach required under **PCT Article 33(3)** and PCT Guidelines. The ISA conflated:

1. **Known use**: Multi-camera broadcasting for viewer experience
2. **Inventive use**: Multi-camera temporal manipulation for security

This is analogous to saying that because hammers are well-known for driving nails, using a hammer as a pendulum weight in a clock would be obvious. The tool may be known, but the application creates a non-obvious technical effect.

### B. Evidence from the Specification

The Applicant explicitly acknowledges prior art multi-camera systems:

**Paragraphs 21-47** describe traditional broadcasting:
- ¶33: "skilled technicians deploying an array of cameras across the venue"
- ¶36: "strategic placement is crucial for creating an immersive viewing experience"
- ¶43: "camera operators spring into action, recording live footage"
- ¶44: "director playing a pivotal role in deciding which camera feeds are broadcast"

**Key distinction** - Traditional purpose (¶36): "creating an immersive viewing experience that mirrors the excitement of being present"

**The invention's purpose** (¶261): "turning every camera cut into an opportunity to enhance content security"

### C. Technical Purpose Comparison

| Aspect                | Traditional Multi-Camera Use | The Invention's Use           |
| --------------------- | ---------------------------- | ----------------------------- |
| **Primary Purpose**   | Enhanced viewing experience  | Content security              |
| **Camera Selection**  | Artistic/editorial choice    | Security algorithm-driven     |
| **Viewer Experience** | All see same feed            | Each sees unique combination  |
| **Technical Effect**  | Better coverage              | Exponential piracy resistance |
| **Infrastructure**    | Standard broadcast           | Same hardware, new purpose    |

## IV. Proper Problem-Solution Analysis Under PCT Guidelines

### A. Step 1: Identifying the Closest Prior Art

Under PCT Guidelines (Part III, Chapter 7.3), the closest prior art must:
1. Be in the same technical field
2. Address a similar problem
3. Have the most features in common

**Proper closest prior art**: Traditional multi-camera broadcasting systems (described in ¶21-93)
- Same field: Multi-camera video production
- Different problem: Entertainment vs. security
- Common features: Multiple cameras, switching capability

**Why D1/D2 are not closest prior art**:
- Different field: Watermarking/pixel manipulation
- Different problem: Protecting embedded data
- Few common features: No multi-camera aspect

### B. Step 2: Objective Technical Problem

Starting from traditional multi-camera broadcasting, the objective technical problem is:

**"How to utilize existing multi-camera broadcast infrastructure to create traceable content variations that resist piracy"**

This problem formulation reveals why the solution is non-obvious:
1. No prior art suggests using camera switching for security
2. The entertainment and security fields have different objectives
3. The technical effect (exponential scalability) is unexpected

### C. Step 3: Would the Skilled Person Arrive at the Solution?

Under the "could-would" approach (PCT Guidelines, Chapter 7.5.3):

**Could** the skilled person use multi-camera systems for security?
- Theoretically possible (cameras exist)

**Would** the skilled person make this leap?
- **No**, because:
  1. Broadcasting aims for consistent viewer experience
  2. Security traditionally uses watermarking (as D1/D2 show)
  3. The paradigm shift requires abandoning both conventions
  4. No suggestion in prior art to vary camera cuts for security

## V. Detailed Technical Analysis of the Inventive Concept

### A. The Repurposing Innovation

The invention's core innovation lies not in multi-camera systems themselves, but in their repurposing through temporal manipulation:

**From paragraph 156-160**:
"The system of the present invention allows to capture an event from various viewpoints using a set of cameras, to process this content through an audio-video production pipeline, and to manage real-time directorial decisions to switch between camera angles"

**Critical addition**: These decisions are "complementarely managed" by the security algorithm, not artistic choice but complementary to it.

**From paragraph 635-639**:
"The invention leverages the inherent complexity of video production and distribution, **turning every camera cut into an opportunity to enhance content security**"

This transformation of purpose is the essence of the invention.

### B. Technical Implementation Differences

| Traditional Broadcasting                        | The Invention                                                 |
| ----------------------------------------------- | ------------------------------------------------------------- |
| Director chooses cameras aesthetically          | Algorithm selects based on security patterns detectable by AI |
| All viewers see identical switches              | Each viewer group sees unique switch patterns                 |
| Switches enhance storytelling                   | Switches create cryptographic-like signatures                 |
| Quality is paramount                            | Quality maintained while adding security layer                |
| Linear scalability (more cameras = more angles) | Exponential scalability ((M+1)^N unique versions)             |

### C. The Non-Obvious Technical Effect

The specification demonstrates unexpected technical effects from this repurposing:

**Exponential Scalability** (¶1427-1429):
"by using a couple of mates in addition to the reference video, the number of different videos would be **1 million after only 100 camera cuts**"

This mathematical relationship (M+1)^N where:
- M = number of mate variations
- N = number of camera cuts

Creates a security space that grows exponentially without additional infrastructure.

**Perfect Synchronization** (¶1390-1392):
All versions remain synchronized to the same master timecode while showing different camera angles, maintaining quality while adding security.

## VI. Response to Specific ISA Objections

### A. Objection: "Multiple Cameras Well-Known"

**Response**: The Applicant agrees! The specification explicitly acknowledges this (¶21-93). However, under **PCT Rule 43bis.1** and the problem-solution approach:

1. **Known feature**: Multiple cameras for broadcasting
2. **Inventive application**: Temporal security through camera selection
3. **Technical effect**: Exponential piracy resistance
4. **Non-obvious because**: No prior art suggests this security application

### B. Objection: "No Technical Synergy"

**Response**: The ISA failed to recognize the synergy between:

1. **Multi-camera infrastructure** (provides variation source)
2. **Driven selection complementary to AI detection** (creates security patterns)
3. **Temporal manipulation** (implements security without quality loss)
4. **Exponential mathematics** (scales security geometrically)

This synergy is evidenced by the mathematical relationship that only emerges from the combination.

### C. Objection: "AI Details Insufficient"

**Response**: The specification provides extensive AI implementation:

**Scene Change Detection** (¶1622-1646):
```python
def extract_middle_third(image_path):
    with Image.open(image_path) as im_pil:
        crop_x1 = 0
        crop_x2 = im_pil.width
        crop_y1 = int(im_pil.height * 0.333)
        crop_y2 = int(im_pil.height * 0.666)
        return im_pil.crop((crop_x1, crop_y1, crop_x2, crop_y2))
```

**Purpose**: Remove broadcaster overlays before temporal analysis

**Fuzzy Matching** (¶1667-1684):
```python
def fuzzy_matching(hashes1, hashes2, max_difference, min_match_percentage):
    num_matches = 0
    for hash1 in hashes1:
        for hash2 in hashes2:
            if abs(hash1 - hash2) <= max_difference:
                num_matches += 1
                break
    percentage_match = num_matches / len(hashes1)
    return percentage_match >= min_match_percentage
```

**Purpose**: Detect pirated content despite temporal shifts from commercials

The AI serves a different purpose than traditional broadcasting:
- **Traditional**: Optimize viewer experience
- **The Invention**: Create and detect security patterns

## VII. Why D1 and D2 Lead Away from the Solution

### A. D1 Teaches Pixel Manipulation

D1 operates entirely in the visual domain:
- ¶[0025]: "transformer 120 applies different transformations to the base copy"
- ¶[0083]: Results in "downgraded quality"

**Why this leads away**: A broadcasting engineer would never intentionally degrade quality

### B. D2 Teaches More Watermarking

D2 adds watermarks at every stage:
- Capture module: "插入水印信息" (insert watermark information)
- Encoding module: "插入编码节点信息" (insert encoding node information)
- Transmission module: Additional encryption
- Decoding module: "插入解码节点信息和水印" (insert decoding node information and watermarks)

**Why this leads away**: Multiplying a failing approach doesn't suggest abandoning it

### C. Neither Suggests Temporal Manipulation

Neither D1 nor D2 mention:
- Camera switching for security
- Temporal patterns as signatures
- Maintaining perfect quality
- Exponential scalability

## VIII. Procedural Matters Under PCT Rules

### A. Prior Art Citation (PCT Rule 5.1(a)(ii))

The ISA noted D1 wasn't cited in the description. Under **PCT Article 34(2)(b)**, the Applicant can amend the description to distinguish D1, though we maintain D1 operates in a different technical field.

### B. Claim Format (PCT Rule 6.3(b))

Regarding two-part form, we propose the following amended claim structure:

### Amended Claim 1 (Two-Part Form):

```text
1. An anti-piracy system (100) for streaming audio-video content captured during live or pre-recorded events using multiple cameras (101) with a production pipeline enabling switches between said cameras called camera cuts,
   characterized in that:
   - the system repurposes said camera cuts from their traditional viewing enhancement function to a security function by comprising:
   - a mate creation component (110) that generates modified versions by automatically altering the temporal positions of camera cuts while maintaining all versions synchronized to identical playback timecodes, wherein different versions show different cameras at the same moment in time;
   - said temporal alterations creating exponentially scalable security where N camera cuts with M mate variations enable (M+1)^N uniquely traceable versions without quality degradation;
   - a detection apparatus applying AI algorithms trained specifically on temporal switching patterns rather than visual content;
   wherein the system achieves content security through editorial domain manipulation rather than pixel domain modification.
```

### C. Unity of Invention (PCT Rules 13.1 and 13.2)

All features contribute to the single inventive concept: repurposing multi-camera infrastructure for exponentially scalable security through temporal manipulation.

## IX. Request for Informal Clarification (PCT Rule 66.2(a))

Given the fundamental misunderstanding about multi-camera usage, the Applicant requests informal clarification under **PCT Rule 66.2(a)(v)** to explain:

1. How known features (cameras) serve a new purpose (security)
2. The temporal vs. visual domain distinction
3. Why exponential scalability is unexpected
4. How synchronization maintains quality

## X. Technical Declaration

Under **PCT Rule 43bis.1**, the Applicant declares all technical effects are fully supported:

1. **Multi-camera acknowledgment**: Paragraphs 21-93
2. **Repurposing for security**: Paragraphs 156-160, 261, 635-639
3. **Exponential scalability**: Paragraphs 622-624, 1427-1429
4. **Zero quality loss**: Abstract, paragraph 547
5. **AI implementation**: Paragraphs 1622-1684

## XI. Analogical Argument

To illustrate why well-known elements can create non-obvious inventions when repurposed:

| Known Element     | Traditional Use | Inventive Repurposing           | Technical Effect              |
| ----------------- | --------------- | ------------------------------- | ----------------------------- |
| **Pendulum**      | Timekeeping     | Foucault's Earth rotation proof | Demonstrates planetary motion |
| **Radio waves**   | Communication   | Radar                           | Object detection              |
| **Cameras**       | Photography     | X-ray imaging                   | See through objects           |
| **Multi-cameras** | Broadcasting    | The Invention                   | Exponential security          |

Each represents a paradigm shift in application, not mere optimization.

## XII. Mathematical Proof of Non-Obviousness

The exponential scaling mathematics only emerges from the specific combination:

**Traditional Broadcasting**:
- 10 cameras = 10 possible views (linear)
- Security = 0 (no consideration)

**Watermarking** (D1/D2):
- Security = f(watermark strength)
- Scalability = linear with processing

**The Invention**:
- Security = (M+1)^N
- Where: M = mates, N = cuts
- Example: 2 mates, 100 cuts = 3^100 = 5×10^47 unique versions

This exponential relationship is neither taught nor suggested by any prior art.

## XIII. Industry Evidence of Non-Obviousness

The specification notes (¶177-192) that even in 2024-2025:
- Industry continues investing in watermarking (as D2 shows)
- AI threats to watermarking are recognized
- Yet no one suggested temporal manipulation

If repurposing multi-camera systems for security were obvious, why does D2 (published 2023) still pursue failed watermarking?

## XIV. Comprehensive Technical Comparison

| Aspect             | Traditional Multi-Camera | D1 (Pixel Transform)   | D2 (Multi-Watermark) | The Invention         |
| ------------------ | ------------------------ | ---------------------- | -------------------- | --------------------- |
| **Purpose**        | Entertainment            | Watermark protection   | Watermark redundancy | Temporal security     |
| **Camera Use**     | Artistic selection       | N/A                    | N/A                  | Security patterns     |
| **Modification**   | None                     | Pixel degradation      | Multiple watermarks  | Temporal only         |
| **Quality**        | Paramount                | Intentionally degraded | Risk of degradation  | Perfect preservation  |
| **Scalability**    | Linear (# cameras)       | Linear (storage)       | Linear (stages)      | Exponential ((M+1)^N) |
| **AI Resistance**  | N/A                      | Vulnerable             | Vulnerable           | Inherent              |
| **Infrastructure** | Standard                 | Standard               | Modified throughout  | Standard repurposed   |

## XV. Formal Requests Under PCT

Based on the foregoing analysis and in accordance with **PCT Article 33(3)** and **PCT Rule 43bis.1**, the Applicant respectfully requests:

1. **Withdrawal** of the inventive step objection, recognizing that repurposing known multi-camera systems for temporal security creates non-obvious technical effects

2. **Acknowledgment** that the invention operates in the temporal/editorial domain, distinct from D1/D2's visual/pixel domain

3. **Recognition** that the exponential scalability mathematics emerges only from the claimed combination

4. **Acceptance** that the AI implementation details exceed typical PCT requirements

5. **Issuance** of a positive Written Opinion under **PCT Article 33(5)**

6. **Alternatively**, an opportunity for informal clarification under **PCT Rule 66.2(a)(v)**

## XVI. Conclusion

The ISA's objection that "multiple cameras are well-known" misses the forest for the trees. Yes, cameras are known - for broadcasting. The invention repurposes this infrastructure for security through temporal manipulation, achieving exponential scalability without quality loss.

This is not an obvious modification but a paradigm shift from:
- Entertainment to security
- Visual to temporal domain
- Linear to exponential scaling
- Quality degradation to perfect preservation

Under the problem-solution approach mandated by **PCT Article 33(3)**, the invention clearly involves an inventive step. The technical effect (exponential security scaling) emerges only from the specific combination claimed and is neither taught nor suggested by any prior art.

The patent system exists to reward exactly such paradigm shifts - taking known elements and repurposing them to solve long-standing problems in non-obvious ways. The Applicant respectfully submits that this invention exemplifies the innovation that PCT examination should recognize and protect.

Respectfully submitted,

[Patent Attorney Name]  
[Registration Number]  
[Firm Name]  
[Date]

---

## Annex A: Visual Representation of Multi-Camera Repurposing

### Traditional Broadcasting (Prior Art):
```
Camera 1 ─┐
Camera 2 ─┼─→ [Director Choice] ─→ [Single Feed] ─→ All Viewers
Camera 3 ─┘
Purpose: Optimal viewing experience
```

### The Invention:
```
Camera 1 ─┐                 ┌─→ Version A (Pattern: 1,2,1,3...)
Camera 2 ─┼─→ Algorithm ─→ ─┼─→ Version B (Pattern: 1,3,2,3...)
Camera 3 ─┘  [AI Security]  └─→ Version C (Pattern: 2,1,3,1...)
                                          ⋮
Purpose: Exponential security versions (3^N possibilities)
```

This visual demonstrates how the same hardware serves an entirely different purpose through the invention's temporal manipulation approach.

## Annex B: Response to Clarity Objections

Under **PCT Article 6**, the following clarifications are provided:

1. **"Time codes of camera cuts"**: Refers to the precise temporal positions (e.g., 00:10:15:03) where camera switches occur, as demonstrated in Tables 1-3 of Example 2

2. **"Distinguishable version"**: Versions that appear visually identical but can be distinguished through temporal pattern analysis of camera switching sequences

3. **"Maintaining temporal synchronization"**: All versions play at the same rate with identical timecodes, differing only in which camera is shown at each moment

These terms have clear technical meaning in the video production field and are further clarified through multiple examples in the specification.