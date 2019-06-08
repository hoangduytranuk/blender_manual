
***********************
Supported Video Formats
***********************

Video Formats
=============

These formats are primarily used for compressing rendered sequences into a playable movie
(they can also be used to make plain audio files).

A codec is a little routine that compresses the video so that it will fit on a DVD,
or be able to be streamed out over the Internet, over a cable, or just be a reasonable file size.
Codecs compress the channels of a video down to save space and enable continuous playback.
*Lossy* codecs make smaller files at the expense of image quality. Some codecs, like H.264,
are great for larger images. Codecs are used to encode and decode the movie,
and so must be present on both the encoding machine (Blender) and the target machine.
The results of the encoding are stored in a container file.

There are dozens, if not hundreds, of codecs, including Xvid, H.264, DivX, Microsoft,
and so on. Each has advantages and disadvantages and compatibility with different players on
different operating systems.

.. note::

   Most codecs can only compress the RGB or YUV :term:`color space`,
   but some support the Alpha channel as well. Codecs that support RGBA include:

   - Quicktime
   - PNG TIFF Pixlet is not lossless, and may be only available on macOS.
   - `Lagarith Lossless Video Codec <http://lags.leetcode.net/codec.html>`__

AVI Codec
   AVI codec compression. Which codecs are available depends on the operating system.
   When an AVI codec is initially chosen, the codec dialog is automatically launched.
   The codec can be changed directly using the *Set Codec* button which appears (*AVI Codec settings.*).
AVI Jpeg
   AVI but with Jpeg compression.
   Lossy, smaller files but not as small as you can get with a Codec compression algorithm.
   Jpeg compression is also the one used in the DV format used in digital camcorders.
AVI Raw
   Audio-Video Interlaced (AVI) uncompressed frames.
H.264
   Encodes movies with the H.264 codec.
MPEG
   Encodes movies with the MPEG codec.
Ogg Theora
   Encodes movies with the Theora codec as Ogg files.
QuickTime
   Apple's Quicktime ``.mov`` file.
   The Quicktime codec dialog is available when this codec is installed on macOS.
   See *Quicktime* in `Video Containers`_.
Xvid
   Encodes movies with the Xvid codec.


Video Containers
================

`MPEG-1 <https://en.wikipedia.org/wiki/MPEG-1>`__: ``.mpg``, ``.mpeg``
   A standard for lossy compression of video and audio.
   It is designed to compress VHS-quality raw digital video and CD audio down to 1.5 Mbit/s.
`MPEG-2 <https://en.wikipedia.org/wiki/MPEG-2>`__: ``.dvd``, ``.vob``, ``.mpg``, ``.mpeg``
   A standard for "the generic coding of moving pictures and associated audio information".
   It describes a combination of lossy video compression and lossy audio data compression
   methods which permit storage and transmission of movies using currently
   available storage media and transmission bandwidth.
`MPEG-4(DivX) <https://en.wikipedia.org/wiki/MPEG-4>`__: ``.mp4``, ``.mpg``, ``.mpeg``
   Absorbs many of the features of MPEG-1 and MPEG-2 and other related standards, and adds new features.
`AVI <https://en.wikipedia.org/wiki/Audio_Video_Interleave>`__: ``.avi``
   A derivative of the Resource Interchange File Format (RIFF), which divides a file's data into blocks, or "chunks".
`Quicktime <https://en.wikipedia.org/wiki/.mov>`__: ``.mov``
   A multi-tracked format. QuickTime and MP4 container formats can use the same MPEG-4 formats;
   they are mostly interchangeable in a QuickTime-only environment.
   MP4, being an international standard, has more support.
`DV <https://en.wikipedia.org/wiki/DV>`__: ``.dv``
   An intra-frame video compression scheme,
   which uses the discrete cosine transform (DCT) to compress video on a frame-by-frame basis.
   Audio is stored uncompressed.
`H.264 <https://en.wikipedia.org/wiki/H.264>`__: ``.avi`` *for now*.
   A standard for video compression, and is currently one of the most commonly used formats for the recording,
   compression, and distribution of high definition video.
`Xvid <https://en.wikipedia.org/wiki/Xvid>`__: ``.avi`` *for now*
   A video codec library following the MPEG-4 standard. It uses ASP features such as b-frames,
   global and quarter pixel motion compensation, lumi masking, Trellis quantization, and H.263,
   MPEG and custom quantization matrices. Xvid is a primary competitor of the DivX Pro Codec.
`Ogg <https://en.wikipedia.org/wiki/Theora>`__: ``.ogg``, ``.ogv``
   A free lossy video compression format.
   It is developed by the Xiph.Org Foundation and distributed without licensing fees.
`Matroska <https://en.wikipedia.org/wiki/Matroska>`__: ``.mkv``
   A free open-standard container format, a file format that can hold an unlimited number of video,
   audio, picture or subtitle tracks in one file.
`Flash <https://en.wikipedia.org/wiki/Flash_Video>`__: ``.flv``
   A container file format used to deliver video over the Internet using Adobe Flash Player.
`Wav <https://en.wikipedia.org/wiki/Wav>`__: ``.wav``
   An uncompressed (or lightly compressed) Microsoft and IBM audio file format.
`Mp3 <https://en.wikipedia.org/wiki/MP3>`__: ``.mp3``
   A highly-compressed, patented digital audio encoding format using a form of lossy data compression.
   It is a common audio format for consumer audio storage, as well as a de facto standard of digital
   audio compression for the transfer and playback of music on digital audio players.


Video Codecs
------------

None
   For audio-only encoding.
`MPEG-1 <https://en.wikipedia.org/wiki/MPEG-1>`__
   See `Video Formats`_.
`MPEG-2 <https://en.wikipedia.org/wiki/MPEG-2>`__
   See `Video Formats`_.
`MPEG-4(DivX) <https://en.wikipedia.org/wiki/MPEG-4>`__
   See `Video Formats`_.
`HuffYUV <https://en.wikipedia.org/wiki/Huffyuv>`__
   Lossless video codec created by Ben Rudiak-Gould which is
   meant to replace uncompressed YCbCr as a video capture format.
`DV <https://en.wikipedia.org/wiki/DV>`__
   See `Video Formats`_.
`H.264 <https://en.wikipedia.org/wiki/H.264>`__
   See `Video Formats`_.
`Xvid <https://en.wikipedia.org/wiki/Xvid>`__
   See `Video Formats`_.
`Theora <https://en.wikipedia.org/wiki/Theora>`__
   See Ogg in `Video Formats`_.
`Flash Video <https://en.wikipedia.org/wiki/Flash_Video>`__
   See `Video Formats`_.
`FFmpeg video codec #1 <https://en.wikipedia.org/wiki/FFV1>`__
   A.K.A. FFV1, a lossless intra-frame video codec.
   It can use either variable length coding or arithmetic coding for entropy coding.
   The encoder and decoder are part of the free, open-source library libavcodec in FFmpeg.


Audio Containers
================

`MP2 <https://en.wikipedia.org/wiki/MPEG-1_Audio_Layer_II>`__
   A lossy audio compression format defined by ISO/IEC 11172-3.
`MP3 <https://en.wikipedia.org/wiki/MP3>`__
   See MP3 in `Video Formats`_ (above).
`AC3 <https://en.wikipedia.org/wiki/Dolby_Digital>`__
   Audio Codec 3, an audio compression technology developed by Dolby Laboratories.
`AAC <https://en.wikipedia.org/wiki/Advanced_Audio_Coding>`__
   Advanced Audio Codec, a standardized, lossy compression and encoding scheme for digital audio.
   -- AAC generally achieves better sound quality than MP3 at similar bit rates.
`Vorbis <https://en.wikipedia.org/wiki/Vorbis>`__
   An open-standard, highly-compressed format comparable to MP3 or AAC.
   -- Vorbis generally achieves better sound quality than MP3 at similar bit rates.
`FLAC <https://en.wikipedia.org/wiki/FLAC>`__
   Free Lossless Audio Codec.
   Digital audio compressed by FLAC's algorithm can typically be reduced to 50-60% of its original size,
   and decompressed into an identical copy of the original audio data.
`PCM <https://en.wikipedia.org/wiki/PCM>`__
   Pulse Code Modulation, a method used to digitally represent sampled analog signals.
   It is the standard form for digital audio in computers and various Blu-ray,
   Compact Disc and DVD formats, as well as other uses such as digital telephone systems.


Known Limitations
=================

Video Output Size
-----------------

Some codecs impose limitations on output size,
``H.264``, for example requires both the height and width to be divisible by 2.
