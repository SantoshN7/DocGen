from django.http import HttpResponse, FileResponse

from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib import messages
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import landscape
from reportlab.platypus import Image
from reportlab.lib.utils import ImageReader
from io import BytesIO

from DOC.models import Student, Document ,Course, Student_Course, Student_Document_log

# Create your views here.
def home(request):
    if request.GET.get('semail')  or request.GET.get('seligibility'):
        try:
            if request.GET.get('semail'):
                student=Student.objects.get(s_email=request.GET.get('semail'))
                if student:
                    request.session['sid']=student.id
                    return redirect('doc')
            elif request.GET.get('seligibility'):
                student=Student.objects.get(s_eligibility=request.GET.get('seligibility'))
                if student:
                    request.session['sid']=student.id
                    return redirect('doc')
        except ObjectDoesNotExist:
            messages.error(request, f'Record doesn\'t exist! ')
            return redirect('home')
    else:
        return render(request,'main/home.html')


def doc(request):
    if  request.session.has_key('sid'):
        documents=Document.objects.all()
        context={
            'docs':documents
        }
        return render(request,'main/doc.html',context)
    else:
        messages.error(request, f'Session not Set!')
        return redirect('home')
    
def genrate(request):
    if request.session.has_key('sid') and request.GET.get('selectD'):
        DocID=int(request.GET.get('selectD')) #str to in Get para
        if DocID == 1:
            #for bonafide
            if checkIFActive(request.session['sid']) and checkDocLog(request.session['sid'],1):
                #calltogenrate
                return redirect ('genrateBonafide')
            else:
                messages.error(request, f'Request denied!')
                return redirect('doc')
        elif DocID == 2:
            #for leaving
            if not checkIFActive(request.session['sid']) and checkDocLog(request.session['sid'],2):
                #calltogenrate
                return redirect('genrateLeaving')
            else:
                messages.error(request, f'Request denied!')
                return redirect('doc')
        else:
            messages.error(request, f'Invalid request')
            return redirect('doc') #Doc_log
        stud=Student.objects.get(id=sid)
        doc=Document.objects.get(id=2)
        Student_Document_log.objects.create(s_id=stud,d_id=doc)
    else:
        messages.error(request, f'Invalid request!')
        return redirect('home')

def deleteSession(request):
    messages.error(request, f'Success!')
    del request.session['sid']
    return redirect('home')

def doc_log(request):
    records=Student_Document_log.objects.all().order_by('-genrated_time')
    context={
            'records':records
        }
    return render(request,'main/doclog.html',context)
        

def genrateBonafide(request):
    if  request.session.has_key('sid'):
        sid=request.session['sid']
        student=Student.objects.filter(id=sid).values('s_name','s_birth_date')
        student_course=Student_Course.objects.filter(s_id=sid).filter(course_status='Ongoing').values('roll_no','c_id')
        course=Course.objects.filter(id=student_course[0].get('c_id')).values('c_name')
        current_date=str(datetime.now().date())
        pdf_file_name=str(student_course[0].get('roll_no'))+'_Bon_'+student[0].get('s_name')
        
        #Doc_log
        stud=Student.objects.get(id=sid)
        doc=Document.objects.get(id=1)
        Student_Document_log.objects.create(s_id=stud,d_id=doc)
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename={}.pdf'.format(pdf_file_name)

        buffer = BytesIO()
        c= canvas.Canvas(buffer,pagesize=landscape(letter))

        c.setFont('Helvetica',14,leading=None)
        c.drawCentredString(415,520,'Progressive Education Society\'s')
        c.setFont('Helvetica-Bold',26,leading=None)
        c.drawCentredString(415,490,'Modern College of Arts, Science & Commerce')
        c.setFont('Helvetica',20,leading=None)
        c.drawCentredString(415,460,'Shivajinager, Pune-411005.AUTONOMOUS')
        c.setFont('Helvetica',24,leading=None)
        c.drawCentredString(415,390,'BONAFIDE CERTIFICATE')

        c.setFont('Helvetica-Bold',14,leading=None)
        c.drawRightString(635,360,'Date:')
   
        c.drawRightString(715,360,current_date)
        
        c.setFont('Helvetica',14,leading=None)
        c.drawString(115,300,'This is/was to certify that Mr/Ms.')
       
        c.setFont('Helvetica-Bold',14,leading=None)
        c.drawString(365,300,student[0].get('s_name'))
        
        c.setFont('Helvetica',14,leading=None)
        c.drawString(90,270,'is/was a BONAFIDE STUDENT of this college, during the academic year 2019-2020 and')
        c.drawString(90,240,'is/was studing in')
        c.setFont('Helvetica-Bold',14,leading=None)
        c.drawString(200,240,'Class:')
        
        c.drawString(250,240,course[0].get('c_name'))
        
        c.drawString(500,240,'Roll no:')
        
        c.drawString(570,240,str(student_course[0].get('roll_no')))
       
        c.setFont('Helvetica',14,leading=None)
        c.drawString(90,210,'His/her birthdate as recorded in the college register is')
        
        c.setFont('Helvetica-Bold',14,leading=None)
        c.drawString(450,210,str(student[0].get('s_birth_date').date()))
        
        c.setFont('Helvetica',14,leading=None)
        c.drawString(90,100,'Place: Pune-05.')
        
        #sign
        sign=ImageReader('./media/Sign.png')
        c.drawImage(sign,550,70,width=50 ,height=80)
        c.setFont('Helvetica',12,leading=None)
        c.drawString(550,50,'REGISTRAR')
        #stamp
        stamp=ImageReader('./media/stamp.jpeg')
        c.drawImage(stamp,300,50,width=100 ,height=100)
        
        #logo
        logo=ImageReader('./media/logo.jpg')
        c.drawImage(logo,30,450,width=80 ,height=100)
        
        c.showPage()
        c.save()

        pdf=buffer.getvalue()
        buffer.close()
        response.write(pdf)       
        return response 
    else:
        messages.error(request, f'Session not Set!')
        return redirect('home')



def genrateLeaving(request):
    if  request.session.has_key('sid'):
        sid=request.session['sid']
        student=Student.objects.filter(id=sid).values('s_name','s_birth_date','s_eligibility')
        student_course=Student_Course.objects.filter(s_id=sid).filter(course_status='Completed').values('roll_no','c_id','e_year','e_seat_no','e_result').last()
        course=Course.objects.filter(id=student_course.get('c_id')).values('c_name')
        current_date=str(datetime.now().date())
        pdf_file_name='_Lev_'+student[0].get('s_name')

        #Doc_log
        stud=Student.objects.get(id=sid)
        doc=Document.objects.get(id=2)
        Student_Document_log.objects.create(s_id=stud,d_id=doc)
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename={}.pdf'.format(pdf_file_name)

        buffer = BytesIO()
        c= canvas.Canvas(buffer)

        c.setFont('Helvetica',14,leading=None)
        c.drawCentredString(300,800,'Progressive Education Society\'s')
        c.setFont('Helvetica-Bold',20,leading=None)
        c.drawCentredString(310,770,'Modern College of Arts, Science & Commerce')
        c.setFont('Helvetica',18,leading=None)
        c.drawCentredString(310,740,'Shivajinager, Pune-411005.AUTONOMOUS')
        c.setFont('Helvetica',24,leading=None)
        c.drawCentredString(300,690,'LEAVING CERTIFICATE')

        c.setFont('Helvetica',14,leading=None)
        c.drawString(25,660,'This is/was to certify that Mr/Ms.')
        
        c.setFont('Helvetica-Bold',14,leading=None)
        c.drawString(235,660,student[0].get('s_name'))

        c.setFont('Helvetica',14,leading=None)
        c.drawString(360,660,'has been a student of this college,')

        c.setFont('Helvetica',14,leading=None)
        c.drawString(60,630,'A) After passing/failing his/her last University/Boards HSC Examinaton in year')
        c.drawString(80,610, 'Feb-2015 he/she has kept terms in this College as shown below.')
        c.setFont('Helvetica-Bold',14,leading=None)
        c.drawString(80,590, 'From June 2015 to June 2020')
        c.setFont('Helvetica',14,leading=None)
        
        c.drawString(60,570,'B) He/She apperared for the following examination in this college since his/her')
        c.drawString(80,550, 'last University examination with the results shown against them:')
    
        
        c.drawString(130,530,'Examination     -')
        c.drawString(130,510,'Year                 -')
        c.drawString(130,490,'Exam Seat No  -')
        c.drawString(130,470,'Result               -')
        #c.drawString(130,450,'Class Obtained -')

        c.setFont('Helvetica-Bold',14,leading=None)
        c.drawString(250,530,course[0].get('c_name'))
        c.drawString(250,510,student_course.get('e_year'))
        c.drawString(250,490,str(student_course.get('e_seat_no')))
        c.drawString(250,470,student_course.get('e_result'))
        #c.drawString(250,450,'First Class')

        c.setFont('Helvetica',14,leading=None)
        c.drawString(60,430,'C) His/Her Permanent Registration No. is ')

        c.setFont('Helvetica-Bold',14,leading=None)
        c.drawString(330,430,str(student[0].get('s_eligibility')))

        c.setFont('Helvetica',14,leading=None)
        c.drawString(60,410,'D) He/She has no books in his/her possession belonging to this college.')
        c.drawString(60,390,'E) Nothing is owning by him/her college dues.')
        c.drawString(60,370,'F) He/She bears a good moral character.')
        c.drawString(60,350,'G) His/Her date of birth as entered in College register is')

        c.setFont('Helvetica-Bold',14,leading=None)
        c.drawString(420,350,str(student[0].get('s_birth_date').date()))

        c.setFont('Helvetica',14,leading=None)
        c.drawString(60,310,'H) His/Her voluntary subject or Group or Subject in which he/she attented the')
        c.drawString(80,290,'courses of instruction in this college was')
        c.setFont('Helvetica-Bold',14,leading=None)
        c.drawString(340,290,'Computer Science.')

        c.setFont('Helvetica',14,leading=None)
        c.drawString(60,270,'I) He/She has satisfactorily kept his/her laboratory journal of practical work in')
        c.drawString(80,250,'Science done by him/her')

        c.drawString(60,230,'J) He/She has satisfactorily gone through the course of Physical Training')
        c.drawString(80,210,'prescribed by the University.He/She exempted from P.T. on medical grounds/')
        c.drawString(80,190,'on the ground of his being a member of the N.C.C./on the grounds of his/her')
        c.drawString(80,170,'active membership of a recognised Major Games of the College team.')
        c.setFont('Helvetica-Bold',12,leading=None)
        c.drawString(60,90,'DATE :')
        c.drawString(100,90,current_date)
        c.drawString(450,90,'REGISTRAR')
         #sign
        sign=ImageReader('./media/Sign.png')
        c.drawImage(sign,460,10,width=50 ,height=80)
    
        #stamp
        stamp=ImageReader('./media/stamp.jpeg')
        c.drawImage(stamp,250,20,width=100 ,height=100)

        logo = ImageReader('./media/logo.jpg') 
        c.drawImage(logo,10,720,width=80,height=100)


        
        c.showPage()
        c.save()

        pdf=buffer.getvalue()
        buffer.close()
        response.write(pdf)       
        return response 
    else:
        messages.error(request, f'Session not Set!')
        return redirect('home')



#functions

def checkIFActive(sid):
    return Student_Course.objects.filter(s_id=sid).filter(course_status='Ongoing').exists()

def checkDocLog(sid,did):
    date_time=Student_Document_log.objects.filter(s_id=sid).filter(d_id=did).values('genrated_time').last()
    if date_time != None and date_time['genrated_time'].date() == datetime.now().date():
        return False
    else:
        return True


