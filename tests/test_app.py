from app import __version__


def test_version():
    assert __version__ == "0.1.0"


def test_split():
    response_text = "\n\n1. Tree\n2. Leaf\n3. Rain\n4. Grass\n5. Sky\n6. Stream\n7. Lake\n8. Pond\n9. Snow\n10. Fog\n11. Mist\n12. Air\n13. Soil\n14. Wood\n15. Bush\n16. Seed\n17. Fawn\n18. Dove\n19. Bear\n20. Wolf\n21. Hawk\n22. Deer\n23. Fox\n24. Mole\n25. Finch\n26. Robin\n27. Oak\n28. Fir\n29. Elm\n30. Ash\n31. Dawn\n32. Tide\n33. Steam\n34. Moss\n35. Frost\n36. Lake\n37."
    lines = response_text.strip().split('\n')
    words = [print(line) for line in lines]
    words = [line.split(' ', 1)[1] for line in lines if len(line.split(' ', 1)) > 1]
    print(words)
