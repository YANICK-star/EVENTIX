/**
 * Eventix Cameroon - Bilingual Internationalization (EN / FR)
 */

const translations = {
    en: {
        // Navigation
        "nav.brand_sub": "Cameroon Smart Events",
        "nav.explore": "Explore",
        "nav.my_passes": "My Passes",
        "nav.organizer_desk": "Organizer Desk",
        "nav.door_scanner": "Door Scanner",
        "nav.host_event": "Host Event",
        "nav.sign_in": "Sign In",
        "nav.get_started": "Get Started",
        "nav.sign_out": "Sign Out",
        "nav.profile": "Profile Settings",
        "nav.django_admin": "Django Admin",
        "nav.signed_in_as": "Signed in as",

        // Hero & Discovery
        "hero.badge": "Cameroon Smart Event Ecosystem",
        "hero.title_1": "Never Overbook.",
        "hero.title_2": "Never Gate-Crash.",
        "hero.desc": "Discover academic conferences, musical festivals, sporting matches, and private milestones with atomic seat reservation and instant QR entrance check-in.",
        "hero.search_placeholder": "Search events, seminars, concerts, venues...",
        "hero.search_btn": "Search",
        "hero.all_cities": "All Cameroon Cities",
        "hero.all_categories": "All Categories",
        "hero.filter_type": "Filter Type:",
        "hero.type_all": "All Types",
        "hero.type_academic": "Academic & Seminars",
        "hero.type_entertainment": "Entertainment & Concerts",
        "hero.type_sports": "Sports & Matches",
        "hero.type_private": "Private Milestones",

        // Metrics Strip
        "metric.active_events": "Active Events",
        "metric.passes_reserved": "Passes Reserved",
        "metric.overbook_proof": "Overbook Proof",
        "metric.qr_checkin": "Door QR Check-in",

        // Events Listing
        "events.upcoming_title": "Upcoming Events",
        "events.upcoming_subtitle": "Browse and reserve verified seating for premier events across Cameroon",
        "events.reset_filters": "Reset Filters",
        "events.free_rsvp": "FREE / RSVP",
        "events.seating_capacity": "Seating Capacity",
        "events.seats_left": "seats left",
        "events.sold_out": "SOLD OUT",
        "events.view_reserve": "View & Reserve Pass",
        "events.seating_full": "Seating Full",
        "events.no_events": "No Events Found",
        "events.no_events_desc": "There are currently no events matching your selected city or search keywords.",
        "events.browse_all": "Browse All Events",

        // Detail Page
        "detail.about_title": "About This Event",
        "detail.date_time": "Date & Time",
        "detail.location_venue": "Location & Venue",
        "detail.organized_by": "Organized by",
        "detail.verified_host": "Verified Host",
        "detail.edit_event": "Edit Event",
        "detail.protocol_title": "Eventix Smart Entrance Protocol",
        "detail.protocol_1": "Every booked pass generates a cryptographic, non-replicable digital QR pass.",
        "detail.protocol_2": "Door ushers scan passes using web cameras to prevent duplicate entry or screenshots.",
        "detail.protocol_3": "Strict capacity locking guarantees reserved seating and catering headcounts.",
        "detail.ticket_price": "Ticket Price",
        "detail.per_pass": "Per ticket pass",
        "detail.free_rsvp_desc": "Zero cost entry",
        "detail.live_availability": "Live Seat Availability:",
        "detail.num_passes": "Number of Passes",
        "detail.guest_note": "Guest Note / Special Requests",
        "detail.total_due": "Total Due:",
        "detail.reserve_btn": "Reserve Seating Instantly",
        "detail.sign_in_to_book": "Sign In to Book Pass",
        "detail.new_account": "New to Eventix? Create Free Account",
        "detail.have_passes": "You Have Confirmed Passes!",
        "detail.view_qr_ticket": "View QR Ticket Pass",

        // Ticket Boarding Pass
        "ticket.back": "Back to My Passes",
        "ticket.print": "Print / Save PDF",
        "ticket.cancel": "Cancel Booking",
        "ticket.verified_cred": "Verified Entry Credential",
        "ticket.valid_ready": "VALID · READY TO SCAN",
        "ticket.checked_in": "CHECKED IN",
        "ticket.cancelled": "CANCELLED",
        "ticket.attendee_name": "Attendee Name",
        "ticket.reserved_seats": "Reserved Seats",
        "ticket.total_amount": "Total Amount",
        "ticket.booking_date": "Date of Booking",
        "ticket.gate_token": "Cryptographic Gate Access Token",
        "ticket.qr_instructions": "Present this QR code on your mobile screen or printed pass to the event usher at the entrance.",

        // Organizer Dashboard
        "org.desk_badge": "Organizer Command Desk",
        "org.workspace_title": "Workspace",
        "org.workspace_sub": "Monitor real-time capacities, manage door admissions, and export attendee manifests.",
        "org.open_scanner": "Open Door Scanner",
        "org.create_event": "Create New Event",
        "org.stat_hosted": "Events Hosted",
        "org.stat_bookings": "Total Bookings",
        "org.stat_verified": "Gate Verified",
        "org.stat_revenue": "Gross Ticket Value",
        "org.portfolio_title": "My Events Portfolio",
        "org.th_details": "Event Details",
        "org.th_schedule": "City & Schedule",
        "org.th_seating": "Seating & Occupancy",
        "org.th_checked": "Checked-in",
        "org.th_pricing": "Pricing",
        "org.th_actions": "Actions",

        // Scanner
        "scan.badge": "Instant Gate Verification",
        "scan.title": "Door Check-In Scanner",
        "scan.sub": "Scan attendee QR codes via device web camera or lookup ticket token manually.",
        "scan.for_event": "Scanning For Event:",
        "scan.all_events": "-- All My Events --",
        "scan.viewport_title": "Camera Scanner Viewport",
        "scan.start_cam": "Start Camera",
        "scan.stop_cam": "Stop Camera",
        "scan.manual_title": "Manual Token Lookup",
        "scan.manual_desc": "If guest phone camera or paper is damaged, enter the ticket code:",
        "scan.validate_btn": "Validate Token",
        "scan.recent_title": "Recent Scans",
        "scan.no_scans": "No tickets verified yet this session.",

        // Theme & Lang
        "theme.toggle_dark": "Dark Mode",
        "theme.toggle_light": "Light Mode",
        "lang.en": "English",
        "lang.fr": "Français",

        // Footer
        "footer.tagline": "Cameroon's smart event management ecosystem. Solving venue overcrowding, counterfeit paper ticketing, and slow gate queues with atomic capacity locking and instant QR door verification.",
        "footer.hubs": "Yaoundé & Douala Hubs",
        "footer.momo": "XAF / FCFA & MoMo Ready",
        "footer.academic": "Bachelor 3 Software Engineering",
        "footer.rights": "Built with precision for the modern event ecosystem."
    },
    fr: {
        // Navigation
        "nav.brand_sub": "Événements Intelligents Cameroun",
        "nav.explore": "Explorer",
        "nav.my_passes": "Mes Billets",
        "nav.organizer_desk": "Espace Organisateur",
        "nav.door_scanner": "Scanner d'Entrée",
        "nav.host_event": "Publier un Événement",
        "nav.sign_in": "Connexion",
        "nav.get_started": "S'inscrire",
        "nav.sign_out": "Déconnexion",
        "nav.profile": "Paramètres du Profil",
        "nav.django_admin": "Admin Django",
        "nav.signed_in_as": "Connecté en tant que",

        // Hero & Discovery
        "hero.badge": "Écosystème Événementiel Intelligent du Cameroun",
        "hero.title_1": "Zéro Surréservation.",
        "hero.title_2": "Zéro Fraude à l'Entrée.",
        "hero.desc": "Découvrez conférences académiques, festivals musicaux, rencontres sportives et réceptions privées avec réservation atomique et vérification QR instantanée.",
        "hero.search_placeholder": "Rechercher événements, séminaires, concerts, lieux...",
        "hero.search_btn": "Rechercher",
        "hero.all_cities": "Toutes les Villes du Cameroun",
        "hero.all_categories": "Toutes les Catégories",
        "hero.filter_type": "Type d'événement :",
        "hero.type_all": "Tous Types",
        "hero.type_academic": "Académique & Séminaires",
        "hero.type_entertainment": "Spectacles & Concerts",
        "hero.type_sports": "Sports & Matchs",
        "hero.type_private": "Célébrations Privées & Mariages",

        // Metrics Strip
        "metric.active_events": "Événements Actifs",
        "metric.passes_reserved": "Billets Réservés",
        "metric.overbook_proof": "Anti-Surréservation",
        "metric.qr_checkin": "Scan QR à l'Entrée",

        // Events Listing
        "events.upcoming_title": "Événements à Venir",
        "events.upcoming_subtitle": "Découvrez et réservez des places vérifiées pour les grands événements au Cameroun",
        "events.reset_filters": "Réinitialiser les Filtres",
        "events.free_rsvp": "GRATUIT / RSVP",
        "events.seating_capacity": "Capacité des Places",
        "events.seats_left": "places restantes",
        "events.sold_out": "COMPLET",
        "events.view_reserve": "Voir & Réserver la Place",
        "events.seating_full": "Salle Complète",
        "events.no_events": "Aucun Événement Trouvé",
        "events.no_events_desc": "Aucun événement ne correspond à vos filtres ou mots-clés actuels.",
        "events.browse_all": "Voir Tous les Événements",

        // Detail Page
        "detail.about_title": "À Propos de Cet Événement",
        "detail.date_time": "Date & Heure",
        "detail.location_venue": "Lieu & Salle",
        "detail.organized_by": "Organisé par",
        "detail.verified_host": "Hôte Vérifié",
        "detail.edit_event": "Modifier l'Événement",
        "detail.protocol_title": "Protocole d'Entrée Sécurisé Eventix",
        "detail.protocol_1": "Chaque billet réservé génère un pass numérique QR cryptographique non reproductible.",
        "detail.protocol_2": "Les hôtesses scannent les pass par caméra pour éliminer les captures d'écran et doublons.",
        "detail.protocol_3": "Le verrouillage atomique garantit le nombre exact de chaises et de couverts.",
        "detail.ticket_price": "Prix du Billet",
        "detail.per_pass": "Par billet d'accès",
        "detail.free_rsvp_desc": "Entrée libre sur confirmation",
        "detail.live_availability": "Places Disponibles en Direct :",
        "detail.num_passes": "Nombre de Places",
        "detail.guest_note": "Remarque / Demande Spéciale",
        "detail.total_due": "Total à Régler :",
        "detail.reserve_btn": "Réserver ma Place Immédiatement",
        "detail.sign_in_to_book": "Connectez-vous pour Réserver",
        "detail.new_account": "Nouveau sur Eventix ? Créer un Compte Gratuit",
        "detail.have_passes": "Vous Avez des Billets Confirmés !",
        "detail.view_qr_ticket": "Voir le Pass Billet QR",

        // Ticket Boarding Pass
        "ticket.back": "Retour à Mes Billets",
        "ticket.print": "Imprimer / Enregistrer PDF",
        "ticket.cancel": "Annuler la Réservation",
        "ticket.verified_cred": "Titre d'Accès Sécurisé Vérifié",
        "ticket.valid_ready": "VALIDE · PRÊT POUR SCAN",
        "ticket.checked_in": "ENTRÉE VALIDÉE",
        "ticket.cancelled": "ANNULÉ",
        "ticket.attendee_name": "Nom du Participant",
        "ticket.reserved_seats": "Places Réservées",
        "ticket.total_amount": "Montant Total",
        "ticket.booking_date": "Date de Réservation",
        "ticket.gate_token": "Jeton d'Accès Cryptographique",
        "ticket.qr_instructions": "Présentez ce QR code sur votre écran de téléphone ou pass imprimé à l'hôtesse à la porte d'entrée.",

        // Organizer Dashboard
        "org.desk_badge": "Poste de Commande Organisateur",
        "org.workspace_title": "Espace de Gestion",
        "org.workspace_sub": "Suivez les jauges en temps réel, validez les entrées et exportez les listes d'émargement.",
        "org.open_scanner": "Ouvrir le Scanner de Porte",
        "org.create_event": "Créer un Nouvel Événement",
        "org.stat_hosted": "Événements Créés",
        "org.stat_bookings": "Réservations Totales",
        "org.stat_verified": "Entrées Validées",
        "org.stat_revenue": "Valeur Brute des Billets",
        "org.portfolio_title": "Portefeuille de Mes Événements",
        "org.th_details": "Détails de l'Événement",
        "org.th_schedule": "Ville & Programme",
        "org.th_seating": "Places & Taux d'Occupation",
        "org.th_checked": "À l'Entrée",
        "org.th_pricing": "Tarif",
        "org.th_actions": "Actions",

        // Scanner
        "scan.badge": "Vérification Instantanée aux Portes",
        "scan.title": "Scanner d'Émargement QR",
        "scan.sub": "Scannez les billets par caméra ou recherchez manuellement le code du pass.",
        "scan.for_event": "Événement Actuel :",
        "scan.all_events": "-- Tous Mes Événements --",
        "scan.viewport_title": "Fenêtre de Caméra du Scanner",
        "scan.start_cam": "Démarrer la Caméra",
        "scan.stop_cam": "Arrêter la Caméra",
        "scan.manual_title": "Recherche Manuelle de Jeton",
        "scan.manual_desc": "Si l'écran du participant est fissuré ou illisible, saisissez le code :",
        "scan.validate_btn": "Valider le Pass",
        "scan.recent_title": "Scans Récents",
        "scan.no_scans": "Aucun billet vérifié durant cette session.",

        // Theme & Lang
        "theme.toggle_dark": "Mode Sombre",
        "theme.toggle_light": "Mode Clair",
        "lang.en": "English",
        "lang.fr": "Français",

        // Footer
        "footer.tagline": "Écosystème intelligent de gestion d'événements au Cameroun. Élimine la surréservation, la fraude de billets et les longues files grâce au verrouillage atomique et au scan QR.",
        "footer.hubs": "Pôles Yaoundé & Douala",
        "footer.momo": "Prêt pour XAF / FCFA & Mobile Money",
        "footer.academic": "Licence 3 Génie Logiciel",
        "footer.rights": "Conçu avec rigueur pour l'écosystème événementiel moderne."
    }
};

let currentLang = localStorage.getItem('eventix-lang') || 'en';

function setLanguage(lang) {
    if (!translations[lang]) return;
    currentLang = lang;
    localStorage.setItem('eventix-lang', lang);
    document.cookie = `eventix_lang=${lang};path=/;max-age=31536000`;
    applyTranslations();

    // Update active state in UI
    const enBtns = document.querySelectorAll('.lang-btn-en');
    const frBtns = document.querySelectorAll('.lang-btn-fr');
    if (lang === 'fr') {
        enBtns.forEach(b => b.classList.remove('font-bold', 'text-sky-600', 'dark:text-sky-400'));
        frBtns.forEach(b => b.classList.add('font-bold', 'text-sky-600', 'dark:text-sky-400'));
    } else {
        frBtns.forEach(b => b.classList.remove('font-bold', 'text-sky-600', 'dark:text-sky-400'));
        enBtns.forEach(b => b.classList.add('font-bold', 'text-sky-600', 'dark:text-sky-400'));
    }
}

function applyTranslations() {
    const dict = translations[currentLang] || translations.en;
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dict[key]) {
            el.innerText = dict[key];
        }
    });

    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (dict[key]) {
            el.setAttribute('placeholder', dict[key]);
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    setLanguage(currentLang);
});
