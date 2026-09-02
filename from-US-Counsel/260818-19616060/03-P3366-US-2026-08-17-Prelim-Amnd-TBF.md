# Preliminary Amendment

> High-fidelity Markdown transcription of [`03-P3366-US-2026-08-17-Prelim-Amnd-TBF.pdf`](./03-P3366-US-2026-08-17-Prelim-Amnd-TBF.pdf) (17 pages). The source PDF is authoritative; this file is a convenience review copy.

**PATENT**

**IN THE UNITED STATES PATENT AND TRADEMARK OFFICE**

| Applicant | STEALTH COMPANY SRL START UP INNOVATIVA | Examiner | To be assigned |
|---|---|---|---|
| Serial No. | To be assigned (U.S. National Stage of PCT/IB2025/051755 filed internationally on February 19, 2025) | Art Unit | To be assigned |
| Filed | Concurrently herewith | Our Ref. | P3366-US |
| For | AI–DRIVEN SYSTEM AND METHOD FOR CONTENT DIFFERENTIATION AND PIRACY TRACEABILITY IN STREAMING MEDIA | Date | August 17, 2026 |
|  |  | Re | Preliminary Amendment |

MAIL STOP: PCT  
Commissioner for Patents  
P.O. Box 1450  
Alexandria, VA 22313-1450

## Preliminary Amendment

Dear Commissioner:

Please enter the following amendments and remarks. All amendments and remarks made herein are without prejudice.

Amendments to the Abstract begin on page 2 of this paper.  
Amendments to the Specification begin on page 3 of this paper.  
Amendments to the Claims begin on page 4 of this paper.  
Remarks begin on page 12 of this paper.

## Amendments to the Abstract

Please replace the Abstract of the specification of the application PCT/IB2025/051755 (published as WO2025181623A1) with the below paragraph:

An anti-piracy system generates recipient-associated distinguishable versions of audio-video content. A reference version follows structured edit instructions identifying source cameras and camera-cut time codes. Mate versions retain ordered camera transitions at selected cuts but place the transitions at different timings, producing intervals in which reference and mate versions contain temporally corresponding frames from different cameras. Manifest files select recipient-associated chunk combinations representing reference-or-mate timing choices across the selected cuts, and a ledger associates delivered manifests with recipients. Camera-cut time codes detected in suspected unauthorized content produce a reconstructed manifest representing detected timing choices. The ledger identifies a recipient whose delivered manifest represents the same timing choice at each selected cut, including at least one mate timing. For a composite distribution, probabilistic fingerprinting compares detected timing choices for portions with recipient-associated sequences to identify multiple contributing recipients, and segmented Tardos processing localizes contributions by content segment.

## Amendments to the Specification

On page 1 of the specification of the application PCT/IB2025/051755 (published as WO2025181623A1), after the title “AI–DRIVEN SYSTEM AND METHOD FOR CONTENT DIFFERENTIATION AND PIRACY TRACEABILITY IN STREAMING MEDIA” please amend the specification by adding the following title and paragraph:

### Cross-Reference to Related Applications

The present application is the U.S. National Stage of International Patent Application No. PCT/IB2025/051755 filed on February 19, 2025, which, in turn, claims priority to U.S. Provisional Patent Application No. 63/557,868 filed on February 26, 2024.

## Amendments to the Claims

This listing of claims will replace all prior versions, and listings, of claims in the application.

### Listing of Claims

**1.-18. (Cancelled)**

**19. (new)** A system for generating recipient-associated distinguishable versions of audio-video content and identifying a recipient associated with a suspected unauthorized distribution of the audio-video content, the system comprising one or more processors and memory storing instructions that, when executed by the one or more processors, cause the system to:

receive video captured from a plurality of cameras and a structured list of edit instructions comprising, for each of a plurality of director-commanded camera cuts, a first edit entry comprising an out-point time code and a first source-camera identifier identifying a first camera of the plurality of cameras as a first source camera, and a following edit entry comprising an in-point time code and a second source-camera identifier identifying a second camera of the plurality of cameras as a second source camera different from the first source camera;

produce reference audio-video content according to the structured list of edit instructions;

generate one or more mates of the reference audio-video content by, for each of a plurality of selected camera cuts among the director-commanded camera cuts, modifying, in the structured list of edit instructions, the out-point time code of the corresponding first edit entry and the in-point time code of the corresponding following edit entry while retaining the first and second source-camera identifiers and the order of the first and second source cameras, such that, for each selected camera cut:

a transition from the first source camera to the second source camera occurs at a reference camera-switch timing in the reference audio-video content and at a mate camera-switch timing different from the reference camera-switch timing in at least one of the one or more mates; and

during a temporal interval between the reference camera-switch timing and the mate camera-switch timing, the reference audio-video content and the at least one mate contain temporally corresponding frames captured by different ones of the first and second source cameras;

segment an ensemble comprising the reference audio-video content and the one or more mates into chunks;

generate a plurality of manifest files pointing to respective combinations of chunks selected from the ensemble, each respective combination of chunks preserving, for each of the plurality of selected camera cuts, a choice between the reference camera-switch timing and the mate camera-switch timing of that selected camera cut, so that the respective combinations of chunks represent respective combinations of timing choices across the plurality of selected camera cuts;

cause delivery of streamed audio-video content to respective recipients according to respective manifest files of the plurality of manifest files;

store, in a ledger, associations between the respective manifest files and the recipients to which the streamed audio-video content was delivered according to the respective manifest files;

receive the suspected unauthorized distribution;

apply a scene-change detection algorithm to the suspected unauthorized distribution to identify a plurality of time codes of camera cuts in the suspected unauthorized distribution;

build one or more reconstructed manifest files from the plurality of identified time codes, the one or more reconstructed manifest files including a reconstructed manifest file representing a detected combination of camera-switch timings across the plurality of selected camera cuts; and

search the ledger to identify a recipient associated with a delivered manifest file representing a recipient-associated combination of timing choices, wherein, for each of the plurality of selected camera cuts, the recipient-associated combination and the detected combination represented by the reconstructed manifest file include the same one of the reference camera-switch timing and the mate camera-switch timing for that selected camera cut, and wherein, for at least one of the plurality of selected camera cuts, that same one is the mate camera-switch timing different from the reference camera-switch timing.

**20. (new)** The system of claim 19, wherein one of the plurality of selected camera cuts is a delayed selected camera cut for which the mate camera-switch timing is later than the reference camera-switch timing, and wherein the instructions cause the system to preserve, in the mate containing the mate camera-switch timing for the delayed selected camera cut, a timing of a subsequent camera cut from the reference audio-video content, thereby restoring synchronization between that mate and the reference audio-video content from the subsequent camera cut onward.

**21. (new)** The system of claim 19, wherein the structured list of edit instructions is an Edit Decision List.

**22. (new)** The system of claim 19, wherein the video is captured live from diverse viewpoints and the structured list of edit instructions records the director-commanded camera cuts as real-time selections among the plurality of cameras.

**23. (new)** The system of claim 19, wherein the instructions cause the system to generate a respective mate for each selected camera cut, each respective mate differing from the reference audio-video content in the modified out-point and in-point time codes for only that selected camera cut.

**24. (new)** The system of claim 19, wherein identifying the plurality of time codes comprises comparing frames of the suspected unauthorized distribution with frames of one or both of the reference audio-video content and the one or more mates using perceptual hashes of the frames.

**25. (new)** The system of claim 24, wherein the comparing comprises fuzzy matching in which perceptual hashes of groups of frames are compared using sliding windows.

**26. (new)** The system of claim 19, wherein the chunks are distributed through a content delivery network using adaptive streaming, the plurality of manifest files is tailored to recipient devices or network conditions, and a mixing process integrates chunks of the reference audio-video content with chunks of the one or more mates and progressively assigns respective manifest files to recipients as additional selected camera cuts become available.

**27. (new)** The system of claim 19, wherein a first manifest file points to a first chunk selected from the reference audio-video content and a second manifest file points to a second chunk selected from one of the one or more mates, the first chunk and the second chunk spanning the same playback interval and having equal playback durations.

**28. (new)** The system of claim 27, wherein, for one of the selected camera cuts:

the first chunk contains frames from the corresponding first source camera before the reference camera-switch timing and frames from the corresponding second source camera after the reference camera-switch timing; and

the second chunk contains frames from the corresponding first source camera before the mate camera-switch timing and frames from the corresponding second source camera after the mate camera-switch timing.

**29. (new)** The system of claim 19, wherein the delivered manifest file and the reconstructed manifest file identify the same respective chunk selections at corresponding manifest positions associated with the plurality of selected camera cuts.

**30. (new)** A method of identifying a recipient associated with a suspected unauthorized distribution of audio-video content, the method comprising:

receiving the suspected unauthorized distribution;

applying a scene-change detection algorithm to the suspected unauthorized distribution to identify a plurality of time codes of camera cuts in the suspected unauthorized distribution;

building one or more reconstructed manifest files from the plurality of identified time codes, the one or more reconstructed manifest files including a reconstructed manifest file representing a detected combination of camera-cut timings across a plurality of camera cuts; and

searching a ledger comprising associations between a plurality of delivered manifest files and respective recipients to identify a recipient associated with a delivered manifest file,

wherein each of the plurality of delivered manifest files identifies a respective combination of chunks selected from an ensemble comprising reference audio-video content and one or more mates of the reference audio-video content, and wherein, for each of the plurality of camera cuts, the reference audio-video content contains an ordered transition from a respective first source camera to a respective second source camera at a respective reference camera-cut timing, and at least one of the one or more mates contains the same ordered transition at a respective different mate camera-cut timing,

wherein each of the plurality of delivered manifest files represents, across the plurality of camera cuts, a recipient-associated combination of choices between the respective reference camera-cut timings and the respective different mate camera-cut timings, and

wherein, for each of the plurality of camera cuts, the recipient-associated combination represented by the delivered manifest file and the detected combination represented by the reconstructed manifest file include the same one of the respective reference camera-cut timing and the respective different mate camera-cut timing, and wherein, for at least one of the plurality of camera cuts, that same one is the respective different mate camera-cut timing detected in the suspected unauthorized distribution.

**31. (new)** The method of claim 30, wherein the delivered manifest file and the reconstructed manifest file identify the same respective chunk selections at corresponding manifest positions associated with the plurality of camera cuts.

**32. (new)** The method of claim 30, wherein the delivered manifest file identifies at least one chunk selected from a mate of the one or more mates, the at least one chunk spans a temporal region of the ensemble containing an ordered transition of one of the plurality of camera cuts, and, during an interval between the respective reference camera-cut timing of that ordered transition and the respective different mate camera-cut timing of that ordered transition in the mate, the reference audio-video content and the mate contain temporally corresponding frames captured by different ones of the respective first and second source cameras.

**33. (new)** A method of identifying a plurality of recipients whose respective delivered streamed audio-video content contributed respective portions to a suspected unauthorized distribution of audio-video content, the method comprising:

accessing a ledger comprising associations between a plurality of delivered manifest files and respective recipients, each delivered manifest file identifying a recipient-associated sequence of chunk selections from an ensemble comprising reference audio-video content and one or more mates of the reference audio-video content, the recipient-associated sequence of chunk selections representing a recipient-associated sequence of timing choices across a plurality of selected camera cuts, wherein, for each selected camera cut, each timing choice is a choice between a reference camera-switch timing at which the reference audio-video content contains an ordered transition from a respective first source camera to a respective second source camera and a mate camera-switch timing different from the reference camera-switch timing at which a respective mate of the one or more mates contains the same ordered transition, and wherein, during an interval between the reference camera-switch timing and the mate camera-switch timing, the reference audio-video content and the respective mate contain temporally corresponding frames captured by different ones of the respective first and second source cameras;

receiving the suspected unauthorized distribution;

applying a scene-change detection algorithm to a plurality of temporal portions of the suspected unauthorized distribution to identify respective time codes of camera cuts corresponding to respective ones of the plurality of selected camera cuts;

determining, for each identified time code, whether the corresponding camera cut in the suspected unauthorized distribution occurs at the reference camera-switch timing or the mate camera-switch timing, thereby deriving a detected sequence of timing choices for the plurality of temporal portions;

applying a probabilistic fingerprinting algorithm to the detected sequence and to the recipient-associated sequences represented by the plurality of delivered manifest files; and

identifying, based on an output of the probabilistic fingerprinting algorithm, a plurality of recipients whose delivered streamed audio-video content contributed respective ones of the plurality of temporal portions to the suspected unauthorized distribution.

**34. (new)** The method of claim 33, wherein the probabilistic fingerprinting algorithm comprises a segmented Tardos fingerprinting algorithm that applies respective Tardos fingerprints to content segments corresponding to the plurality of temporal portions and identifies, for respective temporal portions, respective contributing recipients among the plurality of recipients.

**35. (new)** A method for generating recipient-associated distinguishable versions of audio-video content and identifying a recipient associated with a suspected unauthorized distribution of the audio-video content, the method comprising:

receiving video captured from a plurality of cameras and a structured list of edit instructions comprising, for each of a plurality of director-commanded camera cuts, a first edit entry comprising an out-point time code and a first source-camera identifier identifying a first camera of the plurality of cameras as a first source camera, and a following edit entry comprising an in-point time code and a second source-camera identifier identifying a second camera of the plurality of cameras as a second source camera different from the first source camera;

producing reference audio-video content according to the structured list of edit instructions;

generating one or more mates of the reference audio-video content by, for each of a plurality of selected camera cuts among the director-commanded camera cuts, modifying, in the structured list of edit instructions, the out-point time code of the corresponding first edit entry and the in-point time code of the corresponding following edit entry while retaining the first and second source-camera identifiers and the order of the first and second source cameras, such that, for each selected camera cut:

a transition from the first source camera to the second source camera occurs at a reference camera-switch timing in the reference audio-video content and at a mate camera-switch timing different from the reference camera-switch timing in at least one of the one or more mates; and

during a temporal interval between the reference camera-switch timing and the mate camera-switch timing, the reference audio-video content and the at least one mate contain temporally corresponding frames captured by different ones of the first and second source cameras;

segmenting an ensemble comprising the reference audio-video content and the one or more mates into chunks;

generating a plurality of manifest files pointing to respective combinations of chunks selected from the ensemble, each respective combination of chunks preserving, for each of the plurality of selected camera cuts, a choice between the reference camera-switch timing and the mate camera-switch timing of that selected camera cut, so that the respective combinations of chunks represent respective combinations of timing choices across the plurality of selected camera cuts;

delivering streamed audio-video content to respective recipients according to respective manifest files of the plurality of manifest files;

storing, in a ledger, associations between the respective manifest files and the recipients to which the streamed audio-video content was delivered according to the respective manifest files;

receiving the suspected unauthorized distribution;

applying a scene-change detection algorithm to the suspected unauthorized distribution to identify a plurality of time codes of camera cuts in the suspected unauthorized distribution;

building one or more reconstructed manifest files from the plurality of identified time codes, the one or more reconstructed manifest files including a reconstructed manifest file representing a detected combination of camera-switch timings across the plurality of selected camera cuts; and

searching the ledger to identify a recipient associated with a delivered manifest file representing a recipient-associated combination of timing choices, wherein, for each of the plurality of selected camera cuts, the recipient-associated combination and the detected combination represented by the reconstructed manifest file include the same one of the reference camera-switch timing and the mate camera-switch timing for that selected camera cut, and wherein, for at least one of the plurality of selected camera cuts, that same one is the mate camera-switch timing different from the reference camera-switch timing.

**36. (new)** The method of claim 35, wherein one of the plurality of selected camera cuts is a delayed selected camera cut for which the mate camera-switch timing is later than the reference camera-switch timing, and wherein generating the one or more mates comprises preserving, in the mate containing the mate camera-switch timing for the delayed selected camera cut, a timing of a subsequent camera cut from the reference audio-video content, thereby restoring synchronization between that mate and the reference audio-video content from the subsequent camera cut onward.

**37. (new)** The method of claim 35, wherein identifying the plurality of time codes comprises comparing frames of the suspected unauthorized distribution with frames of one or both of the reference audio-video content and the one or more mates using perceptual hashes of the frames.

**38. (new)** The method of claim 37, wherein the comparing comprises fuzzy matching in which perceptual hashes of groups of frames are compared using sliding windows.

## Remarks

### Introductory Comments

**1.** The present application is the U.S. National Stage of International Patent Application PCT/IB2025/051755 filed on February 19, 2025, which, in turn, claims priority to U.S. Provisional Patent Application No. 63/557,868 filed on February 26, 2024.

The Examiner is respectfully requested to acknowledge this status in the next official action.

### Amendments to the Abstract

**2.** The Abstract has been amended for added clarity and to conform to U.S. practice.

### Amendments to the Specification

**3.** The specification has been amended to make specific reference to earlier filed applications, International Patent Application No. PCT/IB2025/051755 filed on February 19, 2025, which, in turn, claims priority to U.S. Provisional Patent Application No. 63/557,868 filed on February 26, 2024.

**4.** Applicant has also included an indication of the above-mentioned earlier filed applications in an Application Data Sheet (ADS) submitted concurrently herewith indicating that those applications form the basis for the claim of priority of the application at issue.

**5.** In this connection, the Applicant requests that the Examiner acknowledge that the present application correctly claims benefit of the earlier filing dates recited in the specification (i.e., February 19, 2025 and February 26, 2024) in accordance with the provisions of 35 USC 363, 35 USC 371 and 37 CFR 1.78(a)(1)(i) and within the time limit provided by 37 CFR 1.78(a)(1)(ii).

### Amendments to the Claims

**6.** As shown in the "Amendments to the Claims" section herein, Applicant cancels claims 1-18 and adds new claims 19-38. Accordingly, Claims 19-38 are now pending for examination.

**7.** All amendments are being made without prejudice. Applicant reserves the right to reintroduce the canceled claims, the combinations of features claimed in the original claims and/or through those multiple dependencies or to add additional claims either later during prosecution of the present application or in applications related to the present one, such as continuation, divisional, and continuation-in-part applications or any other related applications.

### Support for the New Claims

**8.** The overall architecture recited in new independent claims 19 and 35 is summarized, for example, at page 8, lines 9-26, and is described in detail, for example, with reference to FIG. 1 at pages 13-15, in particular from page 14, line 2, through page 15. These passages describe the mate creation component 110, the transcoding components 120, the manifest files 121 pointing to unique interleaved combinations of chunks 113 of the ensemble 112, the ledger 122, the detection component 130 running a camera cuts detection algorithm 131 that devises time codes from the pirate webcasting and builds reconstructed manifest files 121′, and the retrieval component 140 searching the ledger to identify the associated spectator or group. The preferred manifest embodiment states that the retrieval component searches for delivered manifest files equal to the reconstructed manifest files 121′. Original claims 1, 10, 11, 14 and 15 recite this architecture in claim form. Original claim 1 identifies a distinguishable version matching the suspected unauthorized distribution and original claim 15 recites the equality-based manifest embodiment. In new claims 19 and 35, each selected camera cut retains the same ordered transition from the first source camera to the second source camera at a mate camera-switch timing different from the reference camera-switch timing, with temporally corresponding frames from different source cameras during the interval between those timings. The searched delivered manifest file is one of the recipient-associated timing-choice manifest files generated, delivered and recorded by the claimed process. For each selected camera cut, the recipient-associated combination and the detected combination represented by the reconstructed manifest file include the same reference or mate camera-switch timing, with at least one mate camera-switch timing different from the corresponding reference timing. This complete chain from production to attribution is disclosed, for example, by original claim 1 read with page 12, line 16, through page 13, line 4, by pages 14-16, by original claims 11-15 and 17 and by Examples 1 and 3-5. The same ordered transition and the different-camera interval are concretely illustrated, for example, by Example 2.

As to the production side, the structured list of edit instructions with per-cut out-point and in-point time codes and source-camera identifiers is described, for example, at page 16, lines 18-28, and at page 18, lines 13-17. The direction-neutral mate-generation algorithm appears in, for example, Example 1 at pages 31-32. The metacode alternates between adding and subtracting time, assigns a variation of 1 or -1 and applies the variation to the camera-cut timestamp. Example 2 at pages 33-35, with Tables 1 and 2, provides the concrete delayed species by extending Cut 2, delaying the start of Cut 3 by ten frames and restoring synchronization from Cut 4 onward, thereby supporting, for example, the later-timing and subsequent-resynchronization fallbacks of new claims 20 and 36. The complete direction-neutral paired-entry and intervening different-camera relationship of claims 19 and 35 is supported by, for example, the direction-neutral algorithmic disclosure and original claim 1 read with the concrete relationship illustrated in Example 2. Variation at a plurality of selected camera cuts and generation of additional mates and manifest files are described at, for example, page 16, lines 1-17.

As to distribution and the record of associations, the chunk segmentation, content delivery network distribution with adaptive streaming, manifest tailoring to devices or network conditions, progressive mixing of reference and mate chunks and progressive assignment of individualized manifest files recited together in new claim 26 are described, for example, at page 8, lines 9-21, at page 14, lines 10-21, at page 18, line 23, through page 19, line 12, at page 29, lines 19-27, and at page 40, lines 5-7. Method 200 describes, for example, segmenting step 240 enabling adaptive streaming across varying network conditions and device capabilities and generation step 250 producing manifest files tailored to end user devices and network conditions. Original claims 11 and 12 recite, for example, the adaptive-delivery and progressive-mixing relationships in claim form. The ledger identifying which end user received which manifest file appears, for example, at page 8, lines 15-21, and at page 14, lines 17-21. See also original claims 13 and 14.

As to the single-recipient detection side, including monitor-side method claim 30, the operations of receiving the suspected unauthorized distribution, applying a scene-change detection algorithm to identify time codes of camera cuts, building one or more reconstructed manifest files from the identified time codes and searching the ledger to identify the associated recipient are described, for example, at page 8, lines 15-21, at page 14, line 22, through page 15, and in method form at page 30, lines 1-10, describing the ledger recording step 270, the monitoring step 280 detecting scene changes and devising time codes and the searching step 290. Original claims 15, 16 and 17 recite, for example, the same operations in claim form. Claim 30 identifies the recipient associated with the delivered manifest file representing the same cut-by-cut timing-choice combination as the reconstructed manifest file, including at least one detected different mate timing, and does not require identity of complete manifest syntax or metadata.

Independent claim 33 and dependent claim 34 address multi-contributor attribution without requiring the composite detected sequence to match the complete timing-choice sequence of one delivered manifest file. The colluding-redistribution disclosure at pages 23-26 states, for example, that portions from different copies remain traceable to their original distributions and that the ledger and the recorded chunk combinations identify the accounts involved. The probabilistic and Tardos disclosures at pages 24-26 describe identifying users who contributed to a composite pirate copy. The segmented-Tardos disclosure at pages 25-26 applies fingerprints to content segments to localize pirated segments and colluders. Read with the recipient-associated manifest combinations of pages 14-19, with the camera-cut monitoring and searching operations and with Example 2, these passages connect the collusion processing to sequences of chunk selections representing reference or mate timings of the same ordered transitions, to the intervening interval of temporally corresponding different-camera frames and to the determination, from each detected time code, whether the corresponding cut represents the reference or the mate timing. Generic Tardos processing does not by itself supply that timing-choice structure.

As to the remaining claims, the perceptual hash and fuzzy and sliding-window comparisons of new claims 24, 25, 37 and 38 are described, for example, at page 30, lines 21-28, in Example 5 at pages 40-42 and in original claims 2 and 3. The Edit Decision List implementation of the structured list, new claim 21, is described, for example, at page 16, lines 18-25. Capture of live video from diverse viewpoints and recording of director-commanded real-time camera selections, new claim 22, is recited in original claim 16. The computing environment recited in the system preamble is described, for example, at page 18, lines 1-3, and in original claim 8.

New claim 20 is supported, for example, by Example 2 at pages 33-35, which illustrates a mate transition later than the corresponding reference transition and restoration of synchronization at a subsequent camera cut. New claim 23 is supported, for example, by page 16, lines 1-8, describing further camera cuts spawning additional mates and manifest files, read together with Example 2 at pages 33-35, which provides the concrete single-cut variation at the Cut 2 and Cut 3 boundary. New claim 27 is supported, for example, by page 15, lines 12-16, which states expressly that the reference and mate manifest files point to sets of chunks of equal duration, together with Example 3 at pages 36-38, which shows the respective manifest files selecting different chunks at corresponding positions. New claim 28 is supported, for example, by the corresponding reference and mate chunk positions of Example 3 read together with the source camera sequence and the different reference and mate switch timings of Example 2. New claims 29 and 31 are supported, for example, by the delivered-manifest and reconstructed-manifest relationship at pages 14-15, by the specific chunks referenced at corresponding manifest positions in Example 3 at pages 36-38 and by the disclosure at page 19, lines 20-28, that a unique combination of chunks can be matched to a specific manifest file distributed to a particular spectator or group. New claim 32 is supported, for example, by the delivered-manifest and mate-chunk disclosure at pages 14-15 and in Example 3, read with the retained ordered transition at different timings and the intervening different-camera frames of Example 2. New claim 34 is supported, for example, by the segmented-Tardos disclosure at pages 25-26, read with the passages cited for claim 33. New claim 36 is supported, for example, by Example 2 at pages 33-35 in method-compatible production operations. For claims 23, 28, 29, 31, 32, 33 and 34, the recited relationships are shown, for example, by the cited passages read together rather than by a single passage.

* * * * *

### Conclusion

**9.** If any point requires further explanation, the Examiner is invited to call the undersigned representative at (626) 792-0536.

The Commissioner is authorized to charge any additional fees that may be required or credit overpayment to deposit account no. 50-4194. Please ensure that the Attorney Docket Number is referred to when charging any payments or crediting any overpayments for this application.

I hereby certify that this correspondence is being electronically filed on August 17, 2026 by Stephanie Nunez Dominguez.

/Stephanie Nunez Dominguez/

Respectfully submitted,

/Alessandro Steinfl, Reg. No. 56,448/

Alessandro Steinfl  
Attorney For Applicant  
Reg. No. 56,448

STEINFL + BRUNO LLP  
155 N Lake Ave Ste 800  
Pasadena, CA 91101  
(626) 792-0536 voice
