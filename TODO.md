# Fix Database Data Issue - TODO Steps

## Step 1: ✅ Code Updates Applied (MEDIA + Debug)

## Step 2: Install Pillow for ImageField

```
cd gpcul
pip install Pillow
```

## Step 3: Run Server

```
python manage.py runserver
```

## Step 4: Test Registration

- Visit http://127.0.0.1:8000/register
- Fill ALL fields (especially date YYYY-MM-DD, photo optional)
- Submit → should see "registration successful" message
- Check terminal for DEBUG prints

## Step 5: Verify Data

```
python manage.py shell
>>> from main.models import Student
>>> Student.objects.count()  # Should be 1+
>>> Student.objects.all()
```

## Step 6: Check Admin

```
python manage.py createsuperuser
```

- Visit http://127.0.0.1:8000/admin/main/student/
- Login & see Students

## Step 7: [ ] Mark Complete
