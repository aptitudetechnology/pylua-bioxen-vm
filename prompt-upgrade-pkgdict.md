Here's a prompt to update curator.py to use external package definitions:

---

**Please update curator.py to use external package and profile definitions instead of hardcoded ones.**

**Requirements:**
1. **Remove all hardcoded package dictionaries** (CORE_PACKAGES, NETWORKING_PACKAGES, PARSING_PACKAGES, TESTING_PACKAGES)
2. **Remove hardcoded profiles** from the manifest creation
3. **Add constructor parameters** to accept external packages and profiles:
   - `packages_catalog: Dict[str, Package] = None`
   - `profiles_catalog: Dict[str, Dict] = None`
4. **Use provided catalogs or fall back to empty defaults** if none provided
5. **Update all methods** to use the dynamic catalogs instead of hardcoded ones

**Key changes needed:**
- `__init__` method: Accept and store the external catalogs
- `_load_manifest` method: Use provided profiles instead of hardcoded ones
- All package operations should reference `self.catalog` (which comes from constructor)
- The `get_curator()` convenience function should accept catalog parameters

**Important:** The pkgdict folder exists in the **consuming application**, not in the library itself. The library should be agnostic about where packages/profiles come from - they're injected via constructor parameters.

**Expected usage pattern:**
```python
# In the consuming application:
from pkgdict.bioxen_packages import ALL_PACKAGES
from pkgdict.bioxen_profiles import ALL_PROFILES
from pylua_bioxen_vm_lib.utils.curator import Curator

curator = Curator(packages_catalog=ALL_PACKAGES, profiles_catalog=ALL_PROFILES)
```

This makes the curator library-agnostic while allowing applications to provide their own package definitions and profiles.