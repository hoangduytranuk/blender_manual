        READMEFIRST for Daz-friendly, hip-corrected release
	v1.0, last update July 28, 2010 by B. Hahne
	Web site: www.cgspeed.com (see the motion-capture section)

This READMEFIRST file accompanies the primary Daz-friendly BVH
conversion release of the Carnegie-Mellon University (CMU) Graphics
Lab Motion Capture Database.  See "Where to find stuff" at the bottom
of this file for where to get the BVH conversion and/or the original
CMU dataset.

The original CMU motion capture database isn't in BVH format - it's
in ASF/AMC format.  This BVH conversion release was created by Bruce
Hahne, a hobbyist animator, in the interest of making the data more
available and easily usable by other animators.  I presently (2010)
maintain the web site www.cgspeed.com, where this BVH conversion
release is available within the motion capture section.

This is the third major conversion in an occasional series of
conversions of the CMU BVH data into various forms designed to be easy
for hobbyists to use.  The history so far is: 
  2008: First Motionbuilder-friendly release 
  2009: 3dStudio Max biped-friendly release 
  June 2010: Second (slightly improved) Motionbuilder-friendly release
  July 2010: Daz-character-friendly release

This release is a set of BVH files designed to work seamlessly with
the 3rd-generation (gen3) and 4th-generation (gen4) prerigged
characters from Daz (www.daz3d.com).  These characters include, for
example:
  Aiko3  Victoria3  David3  Michael3  SP3
  Aiko4  Victoria4  SP4

A video tutorial on how to use these BVH files with Daz Studio is
available at cgspeed.com.

I've spot-tested the BVH files from this Daz-friendly conversion in
Daz Studio 3.  In theory they should also work with the Daz gen3 and
gen4 characters within any release of Poser or Carrara, however as of
July 2010 I haven't tested with either of these packages.


This Daz-friendly release is derived from the 2010 (second)
Motionbuilder-friendly release using the following workflow:

1. I ran the Motionbuilder-friendly BVH files through a retargeting
script in Motionbuilder, to retarget them onto the Aiko3 skeleton.

2. I ran the resulting Aiko3-compatible BVH files through a
hip-correction script to work around a sporadic Motionbuilder BVH
export bug.  Motionbuilder 2009 occasionally saves bogus hip rotation
values for some (but not all) frames of an animation when exporting in
BVH format. (Motionbuilder 2011, presently in beta as of this writing,
is much worse - it doesn't even export proper BVH files at all).  The
workaround for this bug was to replace all hip rotation values with
the original rotation values from the motionbuilder-friendly,
pre-retargeting BVH files.

A version of the Daz-friendly BVH files WITHOUT the hip correction
algorithm is also available at cgspeed.com, however that isn't what
you've downloaded with this particular release.


ADVANTAGES AND FEATURES OF THIS RELEASE:

- The BVH files are entirely retargeted to the Daz gen3 and gen4
  skeletons, and should import seamlessly onto these Daz characters
  with no need to mess around with joint renaming or post-import
  rotation corrections.  If you've struggled in the past to use BVH
  files to animate Daz characters, you should give this dataset a try
  or watch the training video - it's very fast to use this BVH release
  with the Daz characters.

- Unlike other attempts at releasing Poser-friendly or Daz-friendly
  conversions of this dataset, this conversion has run the files
  through an actual retargeting algorithm in Motionbuilder.  Other
  attempts at Poser-friendly releases that I've seen contain massive
  joint-snarl and rotation-snarl problems.  This release should avoid
  most of these problems, since Motionbuilder did the heavy lifting.

- Index files: As always, the release includes consolidated indices
  that list the motion filenames and their descriptions.  Both
  spreadsheet and word processor friendly index files are available.

- This Daz-friendly release is based on the latest
  Motionbuilder-friendly BVH release, which provides better leg and
  neck rotation corrections than the 2008 release.  The result is that
  when you animate Daz characters using this Daz-friendly release, you
  typically don't get the problem of the character's head being bent
  down at a severe angle.

- Preserves the 120fps of the original CMU dataset - you get every
  frame from the original capture (both the good and bad data...), not
  a downsampled 30fps version.


CAVEATS:

- The original CMU motion capture data was recorded several years ago
  in a non-profit academic environment by people who weren't necessary
  experts at operating the motion capture system.  The data was never
  cleaned and contains a wide variety of joint-flipping problems
  characteristic of "dirty" motion capture data, when the Vicon
  joint-tracking software makes an incorrect guess about how a joint
  has actually rotated.  All releases of the CMU data preserve these
  joint-flip problems in all of their (ugly) glory.  Typically the only
  way to get rid of them is manually clean the data, which is of
  course a time-consuming and tedious process.  Some of the capture
  data is quite good, but other captures, particularly earlier in the
  numeric series of directories, have a lot of joint-flip problems.

- Because MotionBuilder 2009 has a hip rotation BVH export bug, I've
  run this release of the Daz-friendly data through a hip-correction
  script that, for the most part, does an excellent job of undoing
  Motionbuilder's bug.  However, occasionally this script introduces
  foot-slip / floor-contact problems - see for example animation
  directory 144, file 144_05.bvh.  If you discover an animation in
  this release that you don't like due to foot-slip problems, you
  might want to take a look at the "Daz-friendly, hip-uncorrected" BVH
  release, since I'm also releasing the full set of Daz-friendly BVH
  files PRIOR to application of the hip-correction algorithm.  The
  "hip-uncorrected" release is at cgspeed.com, as usual.

- This release provides 120fps BVH data, as do all of the BVH releases
  I've done so far.  Generally you'll want to set your animation
  software to 30fps (for NTSC), 25fps (for PAL), or 24fps (for film)
  after you've done the BVH import, since these fps rates are what
  most video-editing software will expect.

- These BVH files are not designed to work with non-Daz characters
  such as E-frontier / SmithMicro characters, Miki2, RuntimeDNA
  characters, etc.  I also don't know if they'll work cleanly with
  lesser-known Daz figures such as The Freak, The Girl, etc.

- Since it's impossible to test 2600 different BVH files on a dozen
  different Daz characters within 3 different applications (Daz
  Studio, Carrara, Poser), there are plenty of combinations that might
  give you "interesting" or undesired results.  However, work so far
  within Daz Studio has given positive results.

- Blender users: I have yet to see a successful import of a Daz
  character into Blender, and Blender uses a "z axis up" world
  coordinate system that makes life even more difficult miserable for
  converting a variety of data, so please don't hold your breath
  hoping that this Daz-friendly release will be usable in Blender any
  time soon.


INDEX/INFORMATION FILES: 

Each .zip file in this BVH conversion release should include a copy of
this READMEFIRST.txt file, plus four variations of the same motion
index information:
- cmu-mocap-index-spreadsheet.ods: Open Document / OpenOffice
  spreadsheet format
- cmu-mocap-index-spreadsheet.xls: Microsoft Excel format
- cmu-mocap-index-txt.txt: A simple text file with the index
  information and no commentary.
- cmu-mocap-index-text.rtf: Rich Text Format index information with
  some commentary.


USAGE RIGHTS:

CMU places no restrictions on the use of the original dataset, and I
(Bruce) place no additional restrictions on the use of this particular
BVH conversion.

Here's the relevant paragraph from mocap.cs.cmu.edu:

  Use this data!  This data is free for use in research and commercial
  projects worldwide.  If you publish results obtained using this data,
  we would appreciate it if you would send the citation to your
  published paper to jkh+mocap@cs.cmu.edu, and also would add this text
  to your acknowledgments section: "The data used in this project was
  obtained from mocap.cs.cmu.edu.  The database was created with funding
  from NSF EIA-0196217."


AFFILIATION:  I (Bruce) am not affiliated with and don't speak for
Carnegie-Mellon University, and they don't speak for me. :-)

-----------------------------------------------------------------


CONTACT INFO AND WHERE TO FIND STUFF:
  This BVH conversion release: www.cgspeed.com in the motion capture section.
  Original CMU database (not BVH): mocap.cs.cmu.edu
  AMC2BVH freeware utility: http://vipbase.net/amc2bvh/
  MotionBuilder: www.autodesk.com/motionbuilder
  BVHacker free BVH editing software: http://davedub.co.uk/bvhacker
    BVHacker is designed primarily to create BVH files for SecondLife.

To contact the creator of this BVH conversion release: hahne@io.com

If you like this BVH conversion release, feel free to drop me email
and let me know what you're doing with it.
