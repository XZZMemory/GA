from random import choice
import random


def printListWithTwoDi(name, list):
    times = 0
    for video in range(len(list)):
        for desc in list[video]:
            if desc == 1:
                times = times + 1
    print("VN-Times: " + str(times))
    mat = "{:^2}\t"
    print(str(name))
    for i in range(len(list)):
        if i == 0:
            print(mat.format(" "), end=' ')
            for k in range(len(list[i])):
                print(mat.format(str(k)), end=' ')
            print()
        for j in range(len(list[i])):
            if j == 0:
                print(mat.format(str(i)), end=' ')
            if list[i][j] == 1:
                print(mat.format(str(list[i][j])), end=' ')
            else:
                print(mat.format("  "), end=' ')
        print()
    return times


def getVNTimes(list):
    times = 0
    for video in range(len(list)):
        for desc in list[video]:
            if desc == 1:
                times = times + 1
    return times


def printData(name, data):
    print("执行print函数" + name)
    for i in range(len(data)):
        print(str(i) + ": " + str(data[i]))


def getImportant(data):
    temp = []
    for i in range(len(data)):
        temp.append((data[i], i))
    result = sorted(temp, key=lambda temp: temp[0], reverse=True)
    return result[0][1]


list = [[0.05613748638061533, 0, 0, 0, 0, 0, 0], [0, 0.998120918968383, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 4.5699407258403824e-08, 0], [0.004567780035847013, 1.0, 0, 0, 0, 0, 0],
        [0, 0.9999972085514144, 0.001224243924660251, 0, 0, 0, 0],
        [0.030781110574959025, 0, 0.9999999999387084, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
        [0, 0.01874383013206138, 0.9999999999999999, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
        [0.9422278123362453, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0.0029761193557430454, 0, 0, 1.0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0], [0.022770391533863288, 0, 0, 0, 0, 0, 9.693306046720807e-08],
        [0.006913401846660006, 0, 0, 1.0, 0, 0, 0], [0.01584377727607944, 0, 0, 0, 1.0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0.3454338322461816, 0], [0.10536439973837664, 6.486791426230099e-08, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0], [0.03304053814737684, 0, 0, 0, 0, 0.999999999999599, 0],
        [0, 0, 0, 0, 0, 0, 0.05412219859410161], [0.06071022067330856, 0, 0, 0, 0, 0, 0],
        [0, 0.002209672266334284, 0, 0, 0, 0, 1.0385514063182555e-06], [0, 0, 0, 0, 0, 0, 0],
        [0.00011408841786186841, 0, 0, 0, 0, 0, 0], [0.848760192049435, 0, 0, 0, 0.281186185757345, 0, 0],
        [0.02088773047858028, 0, 0, 0, 0, 0, 0], [0.9772302827280345, 0.0022725524212164894, 0, 0, 0, 0, 0],
        [0.0050155601628988356, 0, 0, 0, 0, 0, 0.9999999999992919]]

list2 = [[0.00021674251129722168, 0.03304053814737681, 0.007871141859450138, 0.011737766657223453, 0.3152924726836782,
          0.00011408841786187842, 0.0045677800358469795, 0.002541481181482501, 0.9422278123362453,
          0.0029761193557430753, 0.002834609609668796, 0.004136823776188134, 0.8453567414814108, 0.9667453381720362,
          0.056137486380615303, 0.01584377727607943, 0.006913401846660044, 0.04618008107140169, 0.06204978266070937,
          0.030781110574959053],
         [0.002209671689947896, 1.7587638677566912e-16, 0.9672968338621171, 0.0008790116122686675,
          0.0013676312338492577, 0.9982440860822992, 0.9809770551624324, 0.9991056908874019, 0.018743830132061354,
          2.604269267927528e-08, 0.997085808665609, 0.9391193985935071, 3.920023631656999e-10, 0.9643071386588127,
          3.178868303064078e-10, 0.9998200060504758, 2.268873176611131e-06, 0.9978808876769378, 3.850733548829478e-08,
          1.856605201868142e-10],
         [0.00025087200475630035, 0.0001165032375044603, 0.9907856809478848, 0.9896837296279162, 0.9693549852946846,
          0.9992702848683729, 1.3978256322941506e-09, 0.0007635130206379418, 0, 0.9919736773915965, 0.9531219462209677,
          1.8757463230203236e-05, 0.9632964934598242, 0.9689716750275862, 0.984047453408601, 0.9968610262795371,
          4.246498007766959e-06, 0.8307133598226257, 0.9900863637587881, 0.974838332371354],
         [0.9852697578886955, 0.9481183939329515, 0.9949796123711082, 0.9992856269635161, 0.9964601797270324,
          0.99855440996834, 0.996068524110698, 0.998405910784062, 0.9852739924758868, 0.9900141592329078,
          0.9977551501426902, 0.9958748033854619, 0.9964885109765668, 0.9495006434394176, 0.9910989389868112,
          0.9997783999673964, 0.9967612188817578, 0.9836339883905679, 0.9954443420473021, 0.9238001465698441],
         [1.9981065864779028e-07, 0.9588589502535755, 0.9853141249580085, 0.975452434510695, 0.9683941031557212,
          0.9965195818394055, 7.916745751162958e-08, 0.9894680925126043, 4.9143640093275696e-08, 0.9122322122901151,
          2.4157907515503673e-10, 0.9740840293134315, 3.581289682355593e-08, 0, 1.0446459251502955e-10, 0,
          0.9587696053714934, 0.8896666027501509, 0.7771533111386192, 0.9627624059879966],
         [0, 0.962935326837745, 0.9622729500545033, 4.920231776893188e-07, 4.370734748666233e-08, 0.9968211137331215, 0,
          4.747256593052918e-12, 5.787472168180433e-07, 0.7693528685254462, 1.0627838526214452e-05,
          2.3812159207805228e-07, 0.00010240947450220511, 0.9633385392525355, 0.9328001927437737, 0.34471719169580284,
          1.987312625811501e-09, 0.941579573716405, 0.0009624370690042669, 6.806027224974099e-08],
         [9.666999057971653e-08, 0.9865188804659457, 6.425014986312434e-07, 0.0001478190375055017,
          1.142324656600757e-09, 1.6601819654701288e-06, 0.05324353236642976, 0.0004960840255896598, 0.9798256950350989,
          0, 0.9960451890561, 0.9903112409520345, 0, 0, 4.6475004908970146e-11, 0, 0.00018804083012082394,
          1.2065767406742397e-10, 9.475118151200302e-05, 1.4414477453546236e-07]]

print(list == list2)
